#!/bin/bash

printf "\n\n\n Please enter the MySQL root password : "
read -s ROOT_PASSWORD

DB_USERNAME='pi'
DB_PASSWORD=$(date | md5sum | head -c12)
DB_SERVER='localhost'
DB_NAME='piSchoolBell'

echo
echo $DB_PASSWORD
echo

mysql -u root -p $ROOT_PASSWORD << DATABASE

CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET = utf8;

CREATE USER IF NOT EXISTS '$DB_USERNAME'@'$DB_SERVER';
SET PASSWORD FOR '$DB_USERNAME'@'$DB_SERVER' = PASSWORD('$DB_PASSWORD');

GRANT ALL ON $DB_NAME.* TO '$DB_USERNAME'@'$DB_SERVER';

USE $DB_NAME;

CREATE TABLE IF NOT EXISTS breaks 
( 
breakId INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
breakName VARCHAR(100) NOT NULL, 
startDate DATE NOT NULL, 
endDate DATE NOT NULL, 
UNIQUE (breakName) 
);

CREATE TABLE IF NOT EXISTS ringTimes 
( 
ringTimeId INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
ringTimeName VARCHAR(100) NOT NULL, 
weekDays VARCHAR(7) DEFAULT '1111100', 
ringTime TIME NOT NULL, 
ringPatternId INT(11) NOT NULL, 
CONSTRAINT weekDays_ringTime UNIQUE (weekDays,ringTime) 
);

CREATE TABLE IF NOT EXISTS ringPatterns 
( 
ringPatternId INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
ringPatternName VARCHAR(100) NOT NULL, 
ringPattern VARCHAR(100) NOT NULL, 
UNIQUE (ringPatternName) 
);

DATABASE

cat > /home/pi/bin/piSchoolBell/mysql-config.ini <<CONFIG
[db]
server = $DB_SERVER
user = $DB_USERNAME
password = $DB_PASSWORD
database = $DB_NAME
CONFIG
