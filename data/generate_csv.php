<?php

$content = file_get_contents(__DIR__ . '/raw/raw.json');
if (false === $content) {
   throw new Exception('missing raw data');
}

$raw = json_decode($content, true);

if (false === $file = fopen('raw/dataset.csv', 'w')) {
   throw new Exception('cant write in raw/dataset.csv');
}

$header = [
    'Map',
    'Visitor/Neutral',
    'PTS',
    'Home/Neutral',
    'PTS',
];
fputcsv($file, $header);

foreach ($raw as $war) {
    $row = [
        'Date' => trim($war['date']),
        'Map' => trim($war['map']),
        'Team1' => trim($war['team1']),
        'Team1 PTS' => trim($war['t1_score']),
        'Team2' => trim($war['team2']),
        'Team2 PTS' => trim($war['t2_score']),
    ];
    fputcsv($file, $row);
}
fclose($file);
