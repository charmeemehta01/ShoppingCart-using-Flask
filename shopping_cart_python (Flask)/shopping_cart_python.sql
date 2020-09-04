-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2020 at 02:45 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shopping_cart_python`
--

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `code` varchar(20) NOT NULL,
  `name` text NOT NULL,
  `image_url` text NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `search_metadata` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`code`, `name`, `image_url`, `price`, `quantity`, `search_metadata`) VALUES
('3DcAM01', 'Crocin 650', 'Crocin.png', 30, 30, 'fever headache bodypain backpain'),
('e2ed', 'Paracetamol Tablet', 'Paracetamol.jpg', 10, 30, 'Fever Headache Muscle Pain Menstrual Cramps Post Immunization Pyrexia Arthritis'),
('ffgsd', 'Honitus', 'Honitus.png', 80, 30, 'Cough'),
('jliy6', 'Strepsils', 'strepsils.jpg', 6, 30, 'mouth throat infections'),
('LPN45', 'Aspirin', 'aspirin.jpg', 3, 30, 'headaches period pains colds flu sprains strains arthritis'),
('nijd7an', 'Combiflam', 'Combiflam.jpg', 29, 30, 'Fever Pain Menstrual Cramps Osteoarthritis Rheumatoid Arthritis Gout'),
('USB02', 'Gelusil', 'Gelusil.png', 88, 30, ' heartburn acid indigestion upset stomach bloating gas'),
('vnc3fb', 'Wikoryl Tablet', 'Wikoryl.jpg', 36.55, 30, 'Cold Common cold Fever Nasal decongestant Itchy throat/skin Headache Allergy Chill Toothache Ear pain Joint pain Periods pain Flu Hypotensive conditions Eye mydriasis Intraocular tension Hay fever Watery eyes Anaphylactic shock Rhinitis Urticaria');

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `user_name` text NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  `account_balance` float NOT NULL,
  `pin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
