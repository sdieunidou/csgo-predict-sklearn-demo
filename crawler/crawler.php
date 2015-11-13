<?php

require_once 'vendor/autoload.php';

use Symfony\Component\DomCrawler\Crawler;
use Symfony\Component\Debug\Debug;

Debug::enable();

function getPage($url) {
    return file_get_contents($url);
}

function determineLastPage(&$pages, $page = 1)
{
    $added = [];

    $offset = ($page-1) * 50;
    $content = getPage('http://www.hltv.org/?pageid=188&statsfilter=5&offset='.$offset);
    $crawler = (new Crawler());
    $crawler->addContent($content);
    $crawler->filter('#location a')->each(function($node) use(&$added) {
        $added[] = $node->attr('href');
    });

    $pages = array_merge($pages, $added);
    if (count($added)) {
        $lastPage = end($added);
        if (preg_match('#offset=([0-9]+)#',$lastPage, $matches)) {
            $lastPage = ((int) $matches[1] / 50) + 1;
            if ($lastPage > $page) {
                determineLastPage($pages, $lastPage);
            }
        }
    }
}

$pages = [];
determineLastPage($pages);
$pages = array_unique($pages);

echo sprintf("The is %d page to crawl\n", count($pages));

$matches = [];
foreach ($pages as $i => $page) {
    echo sprintf("Get page %d on %d\n", $i+1, count($pages));

    $content = getPage('http://www.hltv.org' . $page);
    $crawler = (new Crawler());
    $crawler->addContent($content);

    $crawler->filter('.covMainBoxContent > div > div > div > a')->each(function($node) use(&$matches) {
        $href = $node->attr('href');
        if (preg_match('#matchid#', $href, $m)) {
            $matches[] = $href;
        }
    });
}

echo sprintf("The is %d matchs to crawl\n", count($matches));


$wars = [];
foreach ($matches as $i => $war) {
    echo sprintf("Get match %d on %d\n", $i+1, count($matches));

    $content = getPage('http://www.hltv.org' . $war);
    $crawler = (new Crawler());
    $crawler->addContent($content);

    $players = [];
    $detailNode = $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(7) > div.covMainBoxContent > div > div')->each(function($node) use (&$players) {
        if ($node->filter('[title="headshots"]')->count()) {
            $playerName = $node->filter('div > div > div:nth-child(1) > a')->text();
            $link = $node->filter('div > div > div:nth-child(1) > a')->attr('href');
            $teamName = $node->filter('div > div > div:nth-child(2) > a')->text();
            $kills = (int) $node->filter('div > div > div:nth-child(3)')->text();
            $hs = $node->filter('div > div > div:nth-child(3) > span')->text();
            $assist = $node->filter('div > div > div:nth-child(4)')->text();
            $death = $node->filter('div > div > div:nth-child(5)')->text();
            $ratio = $node->filter('div > div > div:nth-child(6)')->text();
            $rating = $node->filter('div > div > div:nth-child(9)')->text();
            $country = null;

            if (preg_match('#http://static.hltv.org//images/flag/(.+).gif#', $node->filter('div > div > div:nth-child(1) > img')->attr('src'), $regex)) {
                $country = $regex[1];
            }

            $players[] = [
                'name' => $playerName,
                'team' => $teamName,
                'kill'   => $kills,
                'hs'   => str_replace(['(', ')'], [''], $hs),
                'assist' => $assist,
                'death' => $death,
                'ratio' => $ratio,
                'rating' => $rating,
                'link' => $link,
                'country' => $country,
            ];
        }
    });

    $wars[] = [
        'event' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(5) > div > div:nth-child(2) > span > a')->text(),
        'link' => $war,
        'map' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(3) > div > div:nth-child(2)')->text(),
        'team1' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(13) > div > div:nth-child(1) > a')->text(),
        'team2' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(15) > div > div:nth-child(1) > a')->text(),
        't1_ratio' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(13) > div > div:nth-child(2)')->text(),
        't2_ratio' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(15) > div > div:nth-child(2)')->text(),
        'players' => $players,
        't1_score' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(9) > div > div:nth-child(2) > span:nth-child(1)')->text(),
        't2_score' => $crawler->filter('#back > div.mainAreaNoHeadline > div.centerNoHeadline > div > div:nth-child(3) > div.covGroupBoxContent > div:nth-child(9) > div > div:nth-child(2) > span:nth-child(2)')->text(),
    ];
}

echo sprintf("The is %d matchs crawled\n", count($wars));
file_put_contents(__DIR__.'/../data/raw/raw.json', json_encode($wars));
