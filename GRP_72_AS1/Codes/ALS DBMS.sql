-- CREATE DATABASE ALS;

SELECT * FROM MEMBERSHIP;
SELECT * from BOOK;
SELECT * from LOAN;
SELECT * from FINE;
SELECT * FROM FINEPAYMENT;
SELECT * FROM RESERVE;

DROP TABLE IF EXISTS Reserve;
DROP TABLE IF EXISTS FinePayment;
DROP TABLE IF EXISTS Fine;
DROP TABLE IF EXISTS Loan;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Membership;

DROP TABLE IF EXISTS Membership;
CREATE TABLE Membership (
    Membership_ID       VARCHAR(6)           NOT NULL,
    Phone               INT               NOT NULL,
    Name                VARCHAR(300)      NOT NULL,
    Faculty             VARCHAR(50)       NOT NULL,
    Email               VARCHAR(300)      NOT NULL,
    Membership_Status   VARCHAR(50)       CONSTRAINT CHECK (Membership_Status IN ("Active", "Inactive")),
    PRIMARY KEY (Membership_ID)
);

DROP TABLE IF EXISTS Book;
CREATE TABLE Book (
    Accession_No        CHAR(3)           NOT NULL,
    Title               VARCHAR(100)      NOT NULL,
    Author              VARCHAR(100)      NOT NULL,
    ISBN                VARCHAR(13)       NOT NULL,
    Publisher           VARCHAR(50)       NOT NULL,
    Publication_Year    INT               NOT NULL,
    PRIMARY KEY (Accession_No)
);

DROP TABLE IF EXISTS Loan;
CREATE TABLE Loan (
    Loan_ID             CHAR(8)           NOT NULL,
    Accession_No        CHAR(3)           NOT NULL,
    Borrow_Date         DATE              NOT NULL,
    Due_Date            DATE              NOT NULL,
    Membership_ID       CHAR(5)           NOT NULL,
    PRIMARY KEY (Loan_ID),
    FOREIGN KEY (Accession_No) REFERENCES Book (Accession_No) ON UPDATE CASCADE 
														      ON DELETE CASCADE,
    FOREIGN KEY (Membership_ID) REFERENCES Membership (Membership_ID) ON UPDATE CASCADE 
																	  ON DELETE CASCADE
);

DROP TABLE IF EXISTS Fine;
CREATE TABLE Fine (
    Membership_ID       CHAR(5)           NOT NULL,
    Loan_ID             CHAR(8)           NOT NULL,
    Fine_Amount         INT               NOT NULL, -- Return_Date - Due_Date
    Return_Date         DATE              DEFAULT NULL,  
    Due_Date            DATE              NOT NULL,
    PRIMARY KEY (Loan_ID)
);

DROP TABLE IF EXISTS FinePayment;
CREATE TABLE FinePayment (
    Membership_ID       CHAR(5),
    Payment_Date        DATE,
    Payment_Amount      INT,
    PRIMARY KEY (Membership_ID)
    );
    
DROP TABLE IF EXISTS Reserve;
CREATE TABLE Reserve (
    Membership_ID       CHAR(5),
    Accession_No        CHAR(3),
    Reserve_Date        DATE,
    Cancel_Status       CHAR(1) CONSTRAINT CHECK(Cancel_Status IN ("Y", "N")),
    PRIMARY KEY         (Accession_No),
    FOREIGN KEY         (Membership_ID) REFERENCES Membership(Membership_ID) ON DELETE CASCADE
    );
    
INSERT INTO membership VALUES ("A101A", "33336663", "Hermione Granger", "Science", "flying@als.edu", "Active");
INSERT INTO membership VALUES ("A201B", "44327676" , "Sherlock Holmes", "Law", "elementarydrw@als.edu", "Active");
INSERT INTO membership VALUES ("A301C", "14358788", "Tintin", "Engineering", "luvmilu@als.edu", "Active");
INSERT INTO membership VALUES ("A401D", "16091609", "Prinche Hamlet", "FASS", "tobeornot@als.edu", "Active");
INSERT INTO membership VALUES ("A5101E", "19701970", "Willy Wonka", "FASS", "choco1@als.edu", "Active");
INSERT INTO membership VALUES ("A601F", "55548008", "Holly Golightly", "Business", "diamond@als.edu", "Active");
INSERT INTO membership VALUES ("A701G", "18661866", "Raskolnikov", "Law", "oneaxe@als.edu", "Active");
INSERT INTO membership VALUES ("A801H", "38548544", "Patrick Bateman", "Business", "mice@als.edu", "Active");
INSERT INTO membership VALUES ("A901I", "18511851", "Captain Ahab", "Science", "wwhale@als.edu", "Active");

INSERT INTO Book(Accession_No, Title, Author, ISBN, Publisher, Publication_Year) values 
("A01", "A 1984 Story" , "George Orwell", 9790000000001, "Intra S.r.l.s.", 2021),
("A02", "100 anos de soledad" , "Gabriel Garcia Marquez", 9790000000002, "Vintage Espanol", 2017),
("A03", "Brave New World" , "Aldous Huxley", 9790000000003, "Harper Perennial", 2006),
("A04", "Crime and Punishment", "Fyodor Dostoevsky", 9790000000004, "Penguin", 2002),
("A05", "The Lion, The Witch and The Wardrobe", "C.S. Lewis", 9790000000005, "Harper Collins", 2002),
("A06", "Frankenstein" , "Mary Shelley", 9790000000006, "Reader's Library Classics", 2021),
("A07", "The Grapes of Wrath", "John Steinbeck", 9790000000007, "Penguin Classics", 2006),
("A08", "The Adventures of Huckleberry Finn", "Mark Twain", 9790000000008, "SeaWolf Press", 2021),
("A09", "Great Expectations", "Charles Dickens", 9790000000009, "Penguin Classics",2002),
("A10", "Catch-22", "Joseph Heller", 9790000000010, "Simon & Schuster",2011),
("A11", "The Iliad", "Homer", 9790000000011, "Penguin Classics", 1998),
("A12", "Les Miserables", "Victor Hugo", 9790000000012, "Signet",2013),
("A13", "Ulysses", "James Joyce", 9790000000013, "Vintage", 1990),
("A14", "Lolita", "Vladimir Nabokov", 9790000000014, "Vintage", 1989),
("A15", "Atlas Shrugged", "Ayn Rand", 9790000000015, "Dutton", 2005),
("A16", "Perfume", "Patrick Suskind", 9790000000016, "Vintage", 2001),
("A17", "The Metamorphosis", "Franz Kafka", 9790000000017, "12th Media Services", 2017),
("A18", "American Psycho", "Bret Easton Ellis", 9790000000018, "ROBERT LAFFONT", 2019),
("A19", "Asterix the Gaul", "Rene Goscinny, Albert Uderzo", 9790000000019, "Papercutz", 2020),
("A20", "Fahrenheit 451", "Ray Bradbury", 9790000000020, "Simon & Schuster", 2012),
("A21", "Foundation", "Isaac Asimov", 9790000000021, "Bantam Spectra Books", 1991),
("A22", "The Communist Manifesto", "Karl Marx, Friedrich Engels", 9790000000022, "Penguin Classics", 2002),
("A23", "Rights of Man, Common Sense, and Other Political Writings", "Thomas Paine", 9790000000023, "Oxford University Press", 2009),
("A24", "The Prince", "Niccolo Machiavelli", 9790000000024, "Independently published", 2019),
("A25",  "The Wealth of Nations", "Adam Smith", 9790000000025, "Royal Classics", 2021),
("A26", "Don Quijote", "Miguel de Cervantes Saavedra", 9790000000026, "Ecco", 2005),
("A27", "The Second Sex", "Simone de Beauvoir", 9790000000027, "Vintage", 2011),
("A28", "Critique of Pure Reason", "Immanuel Kant", 9790000000028, "Cambridge University Press",1999),
("A29", "On The Origin of Species", "Charles Darwin", 9790000000029, "Signet",2003),
("A30", "Philosophae Naturalis Principia Mathematica", "Isaac Newton", 9790000000030, "University of California Press",2016),
("A31", "The Unbearable Lightness of Being", "Milan Kundera", 9790000000031, "Harper Perennial Modern Classics",2009),
("A32", "The Art of War", "Sun Tzu", 9790000000032, "LSC Communications", 2007),
("A33", "Ficciones", "Jorge Luis Borges", 9790000000033, "Penguin Books", 1999),
("A34", "El Amor en Los Tiempos del Colera", "Gabriel Garcia Marquez", 9790000000034, "Vintage", 2007),
("A35", "Pedro Paramo", "Juan Rulfo", 9790000000035, "Grove Press", 1994),
("A36", "The Labyrinth of Solitude", "Octavio Paz", 9790000000036, "Penguin Books", 2008),
("A37", "Twenty Love Poems and a Song of Despair", "Pablo Neruda", 9790000000037, "Penguin Classics", 2006),
("A38", "QED: The Strange Theory of Light and Matter", "Richard Feynman", 9790000000038, "Princeton University Press", 2014),
("A39", "A Brief History of Time", "Stephen Hawking", 9790000000039, "Bantam", 1996),
("A40", "Cosmos", "Carl Sagan", 9790000000040, "Ballantine Books", 2013),
("A41", "Calculus Made Easy", "Silvanus P. Thompson, Martin Gardner", 9790000000041, "St Martins Pr", 1970),
("A42", "Notes on Thermodynamics and Statistics", "Enrico Fermi", 9790000000042, "University of Chicago Press", 1988),
("A43", "The Federalist", "Alexander Hamilton, James Madison, John Jay", 9790000000043, "Coventry House Publishing", 2015),
("A44", "Second Treatise of Government", "John Lcke, C. B. Macpherson", 9790000000044, "Hackett Publishing Company, Inc.", 1980),
("A45", "The Open Society and Its Enemies", "Karl Popper", 9790000000045, "Princeton University Press", 2020),
("A46", "A People's History of the United States", "Howard Zinn", 9790000000046, "Harper Perennial Modern Classics", 2015),
("A47", "Lord of the Flies", "William Golding", 9790000000047, "Penguin Books", 2003),
("A48", "Animal farm", "George Orwell", 9790000000048, "Wisehouse Classics", 2021),
("A49", "The Old Man and the Sea", "Ernest Hemingway", 9790000000049, "Scribner", 1995),
("A50", "Romance of the Three Kingdoms", "Luo Guanzhong", 9790000000050, "Penguin Books", 2018);
    
    
