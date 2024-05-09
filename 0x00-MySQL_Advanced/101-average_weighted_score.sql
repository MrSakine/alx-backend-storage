-- computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
  DECLARE done BOOL DEFAULT false;
  DECLARE user_id int;
  DECLARE cur CURSOR FOR SELECT id FROM users;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;
  OPEN cur;
  process_update: LOOP
    FETCH cur INTO user_id;
  		IF done = true THEN
  			LEAVE process_update;
  		END IF;
    	UPDATE users SET
    	average_score = (
        SELECT
        SUM(corrections.score * projects.weight) / SUM(projects.weight)
        FROM corrections 
        INNER JOIN projects
        WHERE corrections.user_id = user_id
        AND corrections.project_id = projects.id
    	)
    	WHERE id = user_id;
    END LOOP;
    CLOSE cur;
END $$
DELIMITER ;
