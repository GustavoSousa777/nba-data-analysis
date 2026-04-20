CREATE DATABASE nba_analysis;

USE nba_analysis;

CREATE TABLE nba_players (
    Player VARCHAR(100),
    Pos VARCHAR(10),
    Age INT,
    Tm VARCHAR(10),

    G FLOAT,
    GS FLOAT,
    MP FLOAT,

    FG FLOAT,
    FGA FLOAT,
    FGpct FLOAT,
    `3P` FLOAT,
    `3PA` FLOAT,
    `3Ppct` FLOAT,
    `2P` FLOAT,
    `2PA` FLOAT,
    `2Ppct` FLOAT,
    eFGpct FLOAT,

    FT FLOAT,
    FTA FLOAT,
    FTpct FLOAT,

    ORB FLOAT,
    DRB FLOAT,
    TRB FLOAT,
    AST FLOAT,
    STL FLOAT,
    BLK FLOAT,
    TOV FLOAT,
    PF FLOAT,
    PTS FLOAT,

    PTS_per_min FLOAT,
    AST_per_game FLOAT,
    TRB_per_game FLOAT,
    Score FLOAT,

    Player_Type VARCHAR(20)
);

SELECT DATABASE();
SELECT COUNT(*) FROM nba_players;