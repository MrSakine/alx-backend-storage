-- adds a new correction for a student
DELIMITER $$
CREATE PROCEDURE AddBonus(
  IN user_id INT,
  IN project_name VARCHAR(255), 
  IN score INT)
  BEGIN
    INSERT INTO projects(name)
    SELECT project_name
    FROM DUAL
    WHERE NOT EXISTS
    (SELECT * FROM projects WHERE name = project_name LIMIT 1);
    SET @projectID = (SELECT id FROM projects WHERE name = project_name);
    INSERT INTO corrections(user_id, project_id, score)
    VALUES (user_id, @projectID, score);
  END;$$
DELIMITER ;
