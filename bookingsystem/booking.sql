
-- tables
-- Table: address
CREATE TABLE `address` (
    `id` int NOT NULL AUTO_INCREMENT,
    `address1` varchar(120) NOT NULL,
    `address2` varchar(120) NOT NULL,
    `city` varchar(60) NOT NULL,
    `county` varchar(60) NOT NULL,
    `postcode` varchar(8) NOT NULL,
    CONSTRAINT `address_pk` PRIMARY KEY (`id`)
);

-- Table: auditorium
CREATE TABLE `auditorium` (
    `id` int NOT NULL AUTO_INCREMENT,
    `screen_name` int NOT NULL,
    `row_count` int NOT NULL,
    `column_count` int NOT NULL,
    `cinema_id` int NOT NULL,
    CONSTRAINT `auditorium_pk` PRIMARY KEY (`id`)
);

-- Table: booking_data
CREATE TABLE `booking_data` (
    `id` int NOT NULL,
    `user_id` int NOT NULL,
    
    `movie_title` varchar(256) NOT NULL,
    `screening_start` timestamp NOT NULL,
    `seat_count` int NOT NULL,
    CONSTRAINT `booking_data_pk` PRIMARY KEY (`id`)
);

-- Table: cinema
CREATE TABLE `cinema` (
    `id` int NOT NULL AUTO_INCREMENT,
    `address_id` int NOT NULL,
    `name` varchar(40) NOT NULL,
    CONSTRAINT `cinema_pk` PRIMARY KEY (`id`)
);

-- Table: movie
CREATE TABLE `movie` (
    `id` int NOT NULL AUTO_INCREMENT,
    `title` varchar(256) NOT NULL,
    `director` varchar(256) NULL,
    `description` text NULL,
    `duration_min` int NULL,
    CONSTRAINT `movie_pk` PRIMARY KEY (`id`)
);

-- Table: payment
CREATE TABLE `payment` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `card_number` varchar(16) NOT NULL,
    `card_type` varchar(32) NOT NULL,
    `expiration_date` date NOT NULL,
    CONSTRAINT `payment_pk` PRIMARY KEY (`id`)
);

-- Table: reservation
CREATE TABLE `reservation` (
    `id` int NOT NULL AUTO_INCREMENT,
    `screening_id` int NOT NULL,
    `reserved` bool NULL,
    `paid` bool NULL,
    `active` bool NOT NULL,
    `user_id` int NOT NULL,
    `payment_id` int NOT NULL,
    CONSTRAINT `reservation_pk` PRIMARY KEY (`id`)
);

-- Table: screening
CREATE TABLE `screening` (
    `id` int NOT NULL AUTO_INCREMENT,
    `movie_id` int NOT NULL,
    `auditorium_id` int NOT NULL,
    `screening_start` timestamp NOT NULL,
    `end_time` timestamp NOT NULL,
    UNIQUE INDEX `Projection_ak_1` (`auditorium_id`,`screening_start`),
    CONSTRAINT `screening_pk` PRIMARY KEY (`id`)
);

-- Table: seat
CREATE TABLE `seat` (
    `id` int NOT NULL AUTO_INCREMENT,
    `row` int NOT NULL,
    `number` int NOT NULL,
    `auditorium_id` int NOT NULL,
    CONSTRAINT `seat_pk` PRIMARY KEY (`id`)
);

-- Table: seat_reserved
CREATE TABLE `seat_reserved` (
    `id` int NOT NULL AUTO_INCREMENT,
    `seat_id` int NOT NULL,
    `screening_id` int NOT NULL,
    `reservation_id` int NOT NULL,
    CONSTRAINT `seat_reserved_pk` PRIMARY KEY (`id`)
);

-- Table: user
CREATE TABLE `user` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(32) NOT NULL,
    `password` varchar(100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `first_name` varchar(32) NOT NULL,
    `last_name` varchar(32) NOT NULL,
    `is_admin` tinyint(1) NOT NULL,
    CONSTRAINT `user_pk` PRIMARY KEY (`id`)
) COMMENT 'Employee list (users of system)';

-- foreign keys
-- Reference: Projection_Movie (table: screening)
ALTER TABLE `screening` ADD CONSTRAINT `Projection_Movie` FOREIGN KEY `Projection_Movie` (`movie_id`)
    REFERENCES `movie` (`id`)
	ON DELETE CASCADE;

-- Reference: Projection_Room (table: screening)
ALTER TABLE `screening` ADD CONSTRAINT `Projection_Room` FOREIGN KEY `Projection_Room` (`auditorium_id`)
    REFERENCES `auditorium` (`id`)
	ON DELETE CASCADE;

-- Reference: Reservation_Projection (table: reservation)
ALTER TABLE `reservation` ADD CONSTRAINT `Reservation_Projection` FOREIGN KEY `Reservation_Projection` (`screening_id`)
    REFERENCES `screening` (`id`)
	ON DELETE CASCADE;

-- Reference: Seat_Room (table: seat)
ALTER TABLE `seat` ADD CONSTRAINT `Seat_Room` FOREIGN KEY `Seat_Room` (`auditorium_id`)
    REFERENCES `auditorium` (`id`)
	ON DELETE CASCADE;

-- Reference: Seat_reserved_Reservation_projection (table: seat_reserved)
ALTER TABLE `seat_reserved` ADD CONSTRAINT `Seat_reserved_Reservation_projection` FOREIGN KEY `Seat_reserved_Reservation_projection` (`screening_id`)
    REFERENCES `screening` (`id`)
	ON DELETE CASCADE;

-- Reference: Seat_reserved_Seat (table: seat_reserved)
ALTER TABLE `seat_reserved` ADD CONSTRAINT `Seat_reserved_Seat` FOREIGN KEY `Seat_reserved_Seat` (`seat_id`)
    REFERENCES `seat` (`id`)
	ON DELETE CASCADE;

-- Reference: auditorium_cinema (table: auditorium)
ALTER TABLE `auditorium` ADD CONSTRAINT `auditorium_cinema` FOREIGN KEY `auditorium_cinema` (`cinema_id`)
    REFERENCES `cinema` (`id`)
	ON DELETE CASCADE;

-- Reference: booking_data_user (table: booking_data)
ALTER TABLE `booking_data` ADD CONSTRAINT `booking_data_user` FOREIGN KEY `booking_data_user` (`user_id`)
    REFERENCES `user` (`id`)
	ON DELETE CASCADE;


-- Reference: cinema_address (table: cinema)
ALTER TABLE `cinema` ADD CONSTRAINT `cinema_address` FOREIGN KEY `cinema_address` (`address_id`)
    REFERENCES `address` (`id`)
	ON DELETE CASCADE;

-- Reference: payment_user (table: payment)
ALTER TABLE `payment` ADD CONSTRAINT `payment_user` FOREIGN KEY `payment_user` (`user_id`)
    REFERENCES `user` (`id`)
	ON DELETE CASCADE;

-- Reference: reservation_payment (table: reservation)
ALTER TABLE `reservation` ADD CONSTRAINT `reservation_payment` FOREIGN KEY `reservation_payment` (`payment_id`)
    REFERENCES `payment` (`id`)
	ON DELETE CASCADE;

-- Reference: reservation_user (table: reservation)
ALTER TABLE `reservation` ADD CONSTRAINT `reservation_user` FOREIGN KEY `reservation_user` (`user_id`)
    REFERENCES `user` (`id`)
	ON DELETE CASCADE;

-- Reference: seat_reserved_reservation (table: seat_reserved)
ALTER TABLE `seat_reserved` ADD CONSTRAINT `seat_reserved_reservation` FOREIGN KEY `seat_reserved_reservation` (`reservation_id`)
    REFERENCES `reservation` (`id`)
	ON DELETE CASCADE;

-- End of file.

