CREATE SCHEMA `lahman2017raw` ;

ALTER TABLE `lahman2017raw`.`People` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL ,
ADD PRIMARY KEY (`playerID`);

ALTER TABLE `lahman2017raw`.`Batting` 
CHANGE COLUMN `teamID` `teamID` VARCHAR(8) NOT NULL AFTER `playerID`,
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL ,
CHANGE COLUMN `yearID` `yearID` VARCHAR(6) NOT NULL ,
CHANGE COLUMN `stint` `stint` INT(11) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `yearID`, `teamID`, `stint`);

ALTER TABLE `lahman2017raw`.`Batting` 
ADD CONSTRAINT `player`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`People` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
ALTER TABLE `lahman2017raw`.`Appearances` 
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL FIRST,
CHANGE COLUMN `teamID` `teamID` VARCHAR(8) NOT NULL AFTER `playerID`,
CHANGE COLUMN `yearID` `yearID` VARCHAR(6) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `yearID`, `teamID`);

ALTER TABLE `lahman2017raw`.`Appearances` 
ADD INDEX `team1_idx` (`teamID` ASC);
ALTER TABLE `lahman2017raw`.`Appearances` 
ADD CONSTRAINT `team1`
  FOREIGN KEY (`teamID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
ALTER TABLE `lahman2017raw`.`Fielding` 
CHANGE COLUMN `teamID` `teamID` VARCHAR(8) NOT NULL AFTER `playerID`,
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL ,
CHANGE COLUMN `yearID` `yearID` VARCHAR(6) NOT NULL ,
CHANGE COLUMN `stint` `stint` INT(11) NOT NULL ,
CHANGE COLUMN `lgID` `lgID` VARCHAR(12) NULL ,
CHANGE COLUMN `POS` `POS` VARCHAR(12) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `teamID`, `yearID`, `stint`, `POS`);

ALTER TABLE `lahman2017raw`.`Fielding` 
ADD INDEX `team2_idx` (`teamID` ASC);
ALTER TABLE `lahman2017raw`.`Fielding` 
ADD CONSTRAINT `player4`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`People` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `team2`
  FOREIGN KEY (`teamID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `lahman2017raw`.`Managers` 
CHANGE COLUMN `teamID` `teamID` VARCHAR(8) NOT NULL AFTER `playerID`,
CHANGE COLUMN `inseason` `inseason` VARCHAR(6) NOT NULL AFTER `yearID`,
CHANGE COLUMN `playerID` `playerID` VARCHAR(12) NOT NULL ,
CHANGE COLUMN `yearID` `yearID` VARCHAR(6) NOT NULL ,
ADD PRIMARY KEY (`playerID`, `teamID`, `yearID`, `inseason`);

ALTER TABLE `lahman2017raw`.`Managers` 
DROP FOREIGN KEY `P3`;
ALTER TABLE `lahman2017raw`.`Managers` 
ADD INDEX `t3_idx` (`teamID` ASC, `yearID` ASC);
ALTER TABLE `lahman2017raw`.`Managers` 
ADD CONSTRAINT `p5`
  FOREIGN KEY (`playerID`)
  REFERENCES `lahman2017raw`.`People` (`playerID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `t3`
  FOREIGN KEY (`teamID` , `yearID`)
  REFERENCES `lahman2017raw`.`Teams` (`teamID` , `yearID`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
  
ALTER TABLE `lahman2017raw`.`Teams` 
CHANGE COLUMN `teamID` `teamID` VARCHAR(8) NOT NULL FIRST,
CHANGE COLUMN `yearID` `yearID` VARCHAR(6) NOT NULL ,
ADD PRIMARY KEY (`teamID`, `yearID`);


  
