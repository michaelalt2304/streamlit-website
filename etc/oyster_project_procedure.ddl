CREATE PROCEDURE IF NOT EXISTS add_index(IN idx_name_l varchar(128), IN table_name_l varchar(128), IN col_name_l varchar(128))
       BEGIN

             DECLARE var1 int;
             SELECT COUNT(1) 'Index Is There' into @var1 FROM information_schema.STATISTICS
             WHERE table_schema=DATABASE() AND table_name=table_name_l AND index_name=idx_name_l;
             IF (@var1 = 0) THEN
                 BEGIN
                     SET @sql = CONCAT('CREATE INDEX ', idx_name_l, ' ON ', table_name_l, '(', col_name_l, ')');
                     PREPARE stmt FROM @sql;
                     EXECUTE stmt;
                     DEALLOCATE PREPARE stmt;
                 END;
            END IF;
        END;
