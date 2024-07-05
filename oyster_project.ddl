drop schema if exists test_4;
create schema test_4;
use test_4;


create table people
(
    Username     varchar(64) not null
        primary key,
    Password     varchar(64) null,
    Time_Created timestamp   not null
);

create table raw_files
(
    ID         int auto_increment
        primary key,
    Username   varchar(64)   not null,
    Filepath   varchar(2048) not null,
    Size       varchar(64)   not null,
    Type       varchar(64)   not null,
    Extension  varchar(64)   not null,
    Notes      varchar(2048) not null,
    Width      int           not null,
    Height     int           not null,
    Timestamp  timestamp     not null,
    Local_Path varchar(2048) not null,
    Filename   varchar(64)   not null,
    constraint username_2
        foreign key (Username) references people (Username)
);

create index raw_files_people_Username_fk
    on raw_files (Username);

create table roboflow
(
    ID         int auto_increment
        primary key,
    Api_Key    varchar(64)   not null,
    Workspace  varchar(64)   not null,
    Project    varchar(64)   not null,
    Version    int           not null,
    Download   varchar(64)   not null,
    Username   varchar(64)   not null,
    Timestamp  timestamp     not null,
    Local_Path varchar(2048) not null,
    constraint roboflow_ibfk_1
        foreign key (Username) references people (Username)
);

create table models
(
    ID                     int auto_increment
        primary key,
    Timestamp              timestamp     not null,
    Filepath               varchar(64)   not null,
    Version                int           not null,
    Hyperparams            varchar(2048) null,
    Model_Type             varchar(64)   not null,
    Width_Training_Images  int           not null,
    Height_Training_Images int           not null,
    Roboflow_ID            int           not null,
    Epoch                  int           null,
    Batch                  int           null,
    Size                   varchar(1)    not null,
    Local_Path             varchar(2048) not null,
    constraint models_roboflow_Roboflow_ID_fk
        foreign key (Roboflow_ID) references roboflow (ID)
);

create table annotated_files
(
    Raw_File_ID          int                          not null,
    Model_ID             int                          not null,
    Filepath             varchar(2048)                not null,
    Time_to_Annotate     float                        not null,
    Notes                varchar(2048)                null,
    ID                   int auto_increment
        primary key,
    Timestamp            timestamp                    not null,
    Confidence_Threshold int                          not null,
    Local_Path           varchar(2048) default 'REPL' not null,
    constraint annotated_files_pk
        unique (Model_ID, Confidence_Threshold, Raw_File_ID),
    constraint annotated_files_models_Model_ID_fk
        foreign key (Model_ID) references models (ID),
    constraint annotated_files_raw_files_Raw_File_ID_fk
        foreign key (Raw_File_ID) references raw_files (ID)
);

create table annotated_photos
(
    Ann_File_ID       int not null
        primary key,
    Number_of_Oysters int not null,
    constraint annotated_photos_annotated_files_Ann_File_ID_fk
        foreign key (Ann_File_ID) references annotated_files (ID)
);

create table annotated_videos
(
    Ann_File_ID               int        not null,
    Annotation_Rate           float      null,
    Tracing                   tinyint(1) null,
    Average_Number_of_Oysters float      not null,
    constraint annotated_videos_annotated_files_ID_fk
        foreign key (Ann_File_ID) references annotated_files (ID)
);

create table oysters_in_photo
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

create index Username
    on roboflow (Username);

create table videos
(
    Raw_File_ID int        not null
        primary key,
    FPS         float      not null,
    Color_Order varchar(5) null,
    constraint videos_raw_files_Raw_File_ID_fk
        foreign key (Raw_File_ID) references raw_files (ID)
);

