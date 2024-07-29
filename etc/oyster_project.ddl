create database if not exists test_4;
create schema if not exists test_4;
use test_4;



create table if not exists people
(
    Username     varchar(64) not null
        primary key,
    Password     varchar(64) null,
    Time_Created timestamp   not null
);

create table if not exists feedback
(
    Username                 varchar(64)   not null,
    Rating_Overall           int           null,
    Rating_UI                int           null,
    Rating_Ease_Of_Use       int           null,
    Rating_Applicability     int           null,
    Rating_Speed             int           null,
    Rating_Live_Annotation   int           null,
    Rating_File_Upload       int           null,
    Rating_Annotating_Files  int           null,
    Rating_Gallery           int           null,
    Bugs                     varchar(2048) null,
    Additional_Comments      varchar(2048) null,
    Timestamp                timestamp     not null,
    Additional_Functionality varchar(2048) null,
    How_Use                  varchar(2048) null,
    constraint feedback_people_Username_fk
        foreign key (Username) references people (Username)
);

create table if not exists raw_files
(
    ID         int auto_increment
        primary key,
    Username   varchar(64)                     not null,
    Filepath   varchar(2048) default 'REPLACE' not null,
    Size       varchar(64)                     not null,
    Type       varchar(64)                     not null,
    Extension  varchar(64)                     not null,
    Notes      varchar(2048)                   not null,
    Width      int           default 0         not null,
    Height     int           default 0         not null,
    Timestamp  timestamp                       not null,
    Local_Path varchar(2048) default 'REPLACE' not null,
    Filename   varchar(64)   default 'REPLACE' not null,
    constraint username_2
        foreign key (Username) references people (Username)
);

create table if not exists roboflow
(
    ID         int auto_increment
        primary key,
    Api_Key    varchar(64) default 'REPLACE' not null,
    Workspace  varchar(64)                   not null,
    Project    varchar(64)                   not null,
    Version    int                           not null,
    Download   varchar(64)                   not null,
    Username   varchar(64)                   not null,
    Timestamp  timestamp                     not null,
    Local_Path varchar(2048)                 not null,
    Notes      varchar(2048)                 not null,
    constraint roboflow_ibfk_1
        foreign key (Username) references people (Username)
);

create table if not exists models
(
    ID                     int auto_increment
        primary key,
    Timestamp              timestamp                       not null,
    Filepath               varchar(64)   default 'REPLACE' not null,
    Version                int                             not null,
    Hyperparams            varchar(2048)                   null,
    Model_Type             varchar(64)                     not null,
    Width_Training_Images  int                             not null,
    Height_Training_Images int                             not null,
    Roboflow_ID            int                             not null,
    Epoch                  int                             null,
    Batch                  int                             null,
    Size                   varchar(1)                      not null,
    Local_Path             varchar(2048) default 'REPLACE' not null,
    Notes                  varchar(2048)                   not null,
    Username               varchar(64)                     not null,
    constraint models_people_Username_fk
        foreign key (Username) references people (Username),
    constraint models_roboflow_Roboflow_ID_fk
        foreign key (Roboflow_ID) references roboflow (ID)
);

create table if not exists annotated_files
(
    Raw_File_ID          int                             not null,
    Model_ID             int                             not null,
    Filepath             varchar(2048) default 'REPLACE' not null,
    Time_to_Annotate     float                           not null,
    Notes                varchar(2048)                   null,
    ID                   int auto_increment
        primary key,
    Timestamp            timestamp                       not null,
    Confidence_Threshold int                             not null,
    Local_Path           varchar(2048) default 'REPLACE' not null,
    Name_Labels          tinyint(1)                      not null,
    constraint annotated_files_models_ID_fk
        foreign key (Model_ID) references models (ID),
    constraint annotated_files_raw_files_ID_fk
        foreign key (Raw_File_ID) references raw_files (ID)
);

create table if not exists annotated_photos
(
    Ann_File_ID       int not null
        primary key,
    Number_of_Oysters int not null,
    constraint annotated_photos_annotated_files_Ann_File_ID_fk
        foreign key (Ann_File_ID) references annotated_files (ID)
);

create table if not exists annotated_videos
(
    Ann_File_ID               int                  not null,
    Annotation_Rate           float                null,
    Tracing                   tinyint(1)           null,
    Average_Number_of_Oysters float                not null,
    Fast_Annotation           tinyint(1) default 0 not null,
    Frame_Difference_Factor   float      default 1 not null,
    constraint annotated_videos_annotated_files_ID_fk
        foreign key (Ann_File_ID) references annotated_files (ID)
);

create table if not exists oysters_in_photo
(
    Ann_File_ID int         not null,
    Confidence  float       not null,
    X1          float       not null,
    Class       varchar(64) not null,
    Y1          float       not null,
    X2          float       not null,
    Y2          float       not null,
    Class_Index int         not null,
    constraint oysters_in_photo_annotated_photos_Ann_File_ID_fk
        foreign key (Ann_File_ID) references annotated_photos (Ann_File_ID)
);

CALL add_index('Username', 'roboflow', 'Username');

create table if not exists videos
(
    Raw_File_ID int        not null
        primary key,
    FPS         float      not null,
    Color_Order varchar(5) null,
    constraint videos_raw_files_Raw_File_ID_fk
        foreign key (Raw_File_ID) references raw_files (ID)
);





