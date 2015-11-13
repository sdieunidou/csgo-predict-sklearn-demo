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
        'Map' => $war['map'],
        'Visitor/Neutral' => $war['team1'],
        'PTS' => $war['t1_score'],
        'Home/Neutral' => $war['team2'],
        'PTS' => $war['t2_score'],
    ];
    fputcsv($file, $row);
}
fclose($file);
