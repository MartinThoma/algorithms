-- Step 1: Create TableA and TableB without foreign keys
CREATE TABLE TableA (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    table_b_id INT
);

CREATE TABLE TableB (
    id INT PRIMARY KEY,
    description VARCHAR(100),
    table_a_id INT
);

-- Step 2: Add foreign key constraints after both tables are created
ALTER TABLE TableA
ADD CONSTRAINT fk_table_b FOREIGN KEY (table_b_id) REFERENCES TableB(id);

ALTER TABLE TableB
ADD CONSTRAINT fk_table_a FOREIGN KEY (table_a_id) REFERENCES TableA(id);

-- Insert into TableA with a null reference to TableB
INSERT INTO TableA (id, name, table_b_id) VALUES (1, 'A1', NULL);

-- Insert into TableB with a null reference to TableA
INSERT INTO TableB (id, description, table_a_id) VALUES (1, 'B1', NULL);

-- Update TableA to reference TableB
UPDATE TableA SET table_b_id = 1 WHERE id = 1;

-- Update TableB to reference TableA
UPDATE TableB SET table_a_id = 1 WHERE id = 1;

ALTER TABLE TableA 
ALTER COLUMN table_b_id SET NOT NULL;

ALTER TABLE TableB 
ALTER COLUMN table_a_id SET NOT NULL;