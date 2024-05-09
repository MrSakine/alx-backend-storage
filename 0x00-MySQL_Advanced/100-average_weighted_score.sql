-- computes and store the average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
	UPDATE users SET
	average_score = (
    SELECT
    SUM(corrections.score * projects.weight) / SUM(projects.weight)
    AS average
    FROM corrections 
    INNER JOIN projects
    WHERE corrections.user_id = user_id
    AND corrections.project_id = projects.id
	)
	WHERE id = user_id;
END $$
DELIMITER ;
