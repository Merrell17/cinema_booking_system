-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-11-12 16:49:55.924

-- tables
-- Table: address
CREATE TABLE `address` (
    `id` int NOT NULL,
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
    `name` varchar(32) NOT NULL,
    `seats_no` int NOT NULL,
    `cinema_id` int NOT NULL,
    CONSTRAINT `auditorium_pk` PRIMARY KEY (`id`)
) COMMENT 'seats_no is redundancy (it could be computed by counting Seat.id_seat related to specific room)';

-- Table: cinema
CREATE TABLE `cinema` (
    `id` int NOT NULL,
    `address_id` int NOT NULL,
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
    `is_admin` bool NOT NULL,
    CONSTRAINT `user_pk` PRIMARY KEY (`id`)
) COMMENT 'Employee list (users of system)';

-- foreign keys
-- Reference: Projection_Movie (table: screening)
ALTER TABLE `screening` ADD CONSTRAINT `Projection_Movie` FOREIGN KEY `Projection_Movie` (`movie_id`)
    REFERENCES `movie` (`id`);

-- Reference: Projection_Room (table: screening)
ALTER TABLE `screening` ADD CONSTRAINT `Projection_Room` FOREIGN KEY `Projection_Room` (`auditorium_id`)
    REFERENCES `auditorium` (`id`);

-- Reference: Reservation_Projection (table: reservation)
ALTER TABLE `reservation` ADD CONSTRAINT `Reservation_Projection` FOREIGN KEY `Reservation_Projection` (`screening_id`)
    REFERENCES `screening` (`id`);

-- Reference: Seat_Room (table: seat)
ALTER TABLE `seat` ADD CONSTRAINT `Seat_Room` FOREIGN KEY `Seat_Room` (`auditorium_id`)
    REFERENCES `auditorium` (`id`);

-- Reference: Seat_reserved_Reservation_projection (table: seat_reserved)
ALTER TABLE `seat_reserved` ADD CONSTRAINT `Seat_reserved_Reservation_projection` FOREIGN KEY `Seat_reserved_Reservation_projection` (`screening_id`)
    REFERENCES `screening` (`id`);

-- Reference: Seat_reserved_Seat (table: seat_reserved)
ALTER TABLE `seat_reserved` ADD CONSTRAINT `Seat_reserved_Seat` FOREIGN KEY `Seat_reserved_Seat` (`seat_id`)
    REFERENCES `seat` (`id`);

-- Reference: auditorium_cinema (table: auditorium)
ALTER TABLE `auditorium` ADD CONSTRAINT `auditorium_cinema` FOREIGN KEY `auditorium_cinema` (`cinema_id`)
    REFERENCES `cinema` (`id`);

-- Reference: cinema_address (table: cinema)
ALTER TABLE `cinema` ADD CONSTRAINT `cinema_address` FOREIGN KEY `cinema_address` (`address_id`)
    REFERENCES `address` (`id`);

-- Reference: payment_user (table: payment)
ALTER TABLE `payment` ADD CONSTRAINT `payment_user` FOREIGN KEY `payment_user` (`user_id`)
    REFERENCES `user` (`id`);

-- Reference: reservation_payment (table: reservation)
ALTER TABLE `reservation` ADD CONSTRAINT `reservation_payment` FOREIGN KEY `reservation_payment` (`payment_id`)
    REFERENCES `payment` (`id`);

-- Reference: reservation_user (table: reservation)
ALTER TABLE `reservation` ADD CONSTRAINT `reservation_user` FOREIGN KEY `reservation_user` (`user_id`)
    REFERENCES `user` (`id`);

-- Reference: seat_reserved_reservation (table: seat_reserved)
ALTER TABLE `seat_reserved` ADD CONSTRAINT `seat_reserved_reservation` FOREIGN KEY `seat_reserved_reservation` (`reservation_id`)
    REFERENCES `reservation` (`id`);

-- End of file.

