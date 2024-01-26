CREATE DATABASE book_publishing;

DROP TABLE IF EXISTS author;
CREATE TABLE author (
    full_name       varchar(100)    PRIMARY KEY NOT NULL,
    date_of_birth   varchar(10)     NOT NULL
);

DROP TABLE IF EXISTS owners;
CREATE TABLE owners (
    full_name     varchar(100)  PRIMARY KEY NOT NULL,
    date_of_birth varchar(10)   NOT NULL
);

DROP TABLE IF EXISTS publishing_office;
CREATE TABLE publishing_office (
    id_pub_office           Serial          Primary key,
    name_of_office          varchar(100)    NOT NULL,
    address_of_office       varchar(100)    NOT NULL,
    printing_price_per_page varchar(100)    NOT NULL,
    owners_name             varchar(100)    REFERENCES owners (full_name) NOT NULL
);

DROP TABLE IF EXISTS printery;
CREATE TABLE printery (
    id_printery             Serial          Primary key,
    name_of_printery        varchar(100)    NOT NULL,
    address_of_printery     varchar(100)    NOT NULL,
    pages_per_day           varchar(100)    NOT NULL,
    owners_name             varchar(100)    REFERENCES owners (full_name) NOT NULL
);

DROP TABLE IF EXISTS book;
CREATE TABLE book (
    id_book                 Serial          Primary key,
    name_of_book            varchar(100)    NOT NULL,
    year_of_book            varchar(100)    NOT NULL,
    author_name             varchar(100)    REFERENCES author (full_name) NOT NULL
);

DROP TABLE IF EXISTS work;
CREATE TABLE work (
    id_work                 Serial          Primary key,
    work_name               varchar(100)    NOT NULL,
    work_year               varchar(10)     NOT NULL,
    number_of_pages         varchar(100)    NOT NULL,
    book_id                 INTEGER         REFERENCES book (id_book) NOT NULL
);

DROP TABLE IF EXISTS printing;
CREATE TABLE printing (
    id_print                    Serial          Primary key,
    number_of_books_in_print    varchar(100)    NOT NULL,
    printery_id                 INTEGER         REFERENCES printery (id_printery)               NOT NULL,
    pub_office_id               INTEGER         REFERENCES publishing_office (id_pub_office)    NOT NULL,
    book_id                     INTEGER         REFERENCES book (id_book)                       NOT NULL
);
