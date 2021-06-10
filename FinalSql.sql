CREATE TABLE `Users` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `Username` varchar(255) UNIQUE,
  `Email` varchar(255) UNIQUE,
  `Password` varchar(255),
  `Token` int,
  `Type` varchar(255)
);

CREATE TABLE `Staff` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `UID` int UNIQUE NOT NULL,
  `Name` varchar(255),
  `SSN` varchar(255) UNIQUE,
  `Age` int,
  `Gender` varchar(255),
  `Schedule` varchar(255),
  `Job` varchar(255)
);

CREATE TABLE `Patients` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `UID` int UNIQUE NOT NULL,
  `Name` varchar(255),
  `SSN` varchar(255) UNIQUE,
  `Age` int,
  `Gender` varchar(255),
  `History` varchar(255),
  `Phone` varchar(255)
);

CREATE TABLE `Scans` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `StaffID` int NOT NULL,
  `PatientID` int NOT NULL,
  `Name` varchar(255),
  `Date` date,
  `Time` time,
  `Details` varchar(255),
  `Price` float,
  `PriceID` int,
  `DeviceID` int
);

CREATE TABLE `Appointments` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `StaffID` int NOT NULL,
  `PatientID` int NOT NULL,
  `Name` varchar(255),
  `Details` varchar(255),
  `Date` date,
  `Time` time
);

CREATE TABLE `Devices` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `Serial` varchar(255) UNIQUE,
  `Model` varchar(255),
  `Manufacturer` varchar(255),
  `Specifications` varchar(255),
  `State` varchar(255),
  `Notes` varchar(255),
  `LastMaintenanceDate` Date,
  `LastMaintenanceTime` time
);

CREATE TABLE `Prices` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `Name` varchar(255),
  `Details` varchar(255),
  `Price` float
);

CREATE TABLE `Logs` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `UID` int NOT NULL,
  `Details` varchar(255),
  `Time` time,
  `Date` date
);

CREATE TABLE `Complaint` (
  `ID` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `Name` varchar(255),
  `Email` varchar(255),
  `Problem` varchar(255),
  `Details` varchar(255),
  `Time` time,
  `Date` date
);

ALTER TABLE `Logs` ADD CONSTRAINT `UsersLogs` FOREIGN KEY (`UID`) REFERENCES `Users` (`ID`);

ALTER TABLE `Patients` ADD CONSTRAINT `UsersPatients` FOREIGN KEY (`UID`) REFERENCES `Users` (`ID`);

ALTER TABLE `Staff` ADD CONSTRAINT `UsersStaff` FOREIGN KEY (`UID`) REFERENCES `Users` (`ID`);

ALTER TABLE `Scans` ADD CONSTRAINT `ScansPatients` FOREIGN KEY (`PatientID`) REFERENCES `Patients` (`ID`);

ALTER TABLE `Scans` ADD CONSTRAINT `ScansStaff` FOREIGN KEY (`StaffID`) REFERENCES `Staff` (`ID`);

ALTER TABLE `Scans` ADD CONSTRAINT `ScansPrices` FOREIGN KEY (`PriceID`) REFERENCES `Prices` (`ID`);

ALTER TABLE `Scans` ADD CONSTRAINT `ScansDevices` FOREIGN KEY (`DeviceID`) REFERENCES `Devices` (`ID`);

ALTER TABLE `Appointments` ADD CONSTRAINT `AppointmentsStaff` FOREIGN KEY (`StaffID`) REFERENCES `Staff` (`ID`);

ALTER TABLE `Appointments` ADD CONSTRAINT `AppointmentsPatients` FOREIGN KEY (`PatientID`) REFERENCES `Patients` (`ID`);
