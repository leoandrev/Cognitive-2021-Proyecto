DROP TABLE IF EXISTS Usuario ;

CREATE TABLE IF NOT EXISTS Usuario (
  idUsuario INT NOT NULL AUTO_INCREMENT,
  correo VARCHAR(45) NOT NULL,
  nickname VARCHAR(10) NOT NULL,
  contrasena VARCHAR(15) NOT NULL,
  privilegio VARCHAR(7) NOT NULL,
  PRIMARY KEY (idUsuario),
  UNIQUE INDEX usuario_UNIQUE (nickname ASC) ,
  UNIQUE INDEX correo_UNIQUE (correo ASC) )
ENGINE = InnoDB, CHARSET=latin1;


-- -----------------------------------------------------
-- Table Categoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Categoria;

CREATE TABLE IF NOT EXISTS Categoria (
  idCategoria INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(20) NOT NULL,
  PRIMARY KEY (idCategoria),
  UNIQUE INDEX Categoriacol_UNIQUE (nombre ASC) )
ENGINE = InnoDB, CHARSET=latin1;


-- -----------------------------------------------------
-- Table Libro
-- -----------------------------------------------------
DROP TABLE IF EXISTS Libro ;

CREATE TABLE IF NOT EXISTS Libro (
  idLibro INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(45) NOT NULL,
  autor VARCHAR(45) NOT NULL,
  anio VARCHAR(4) NOT NULL,
  edicion VARCHAR(10) NOT NULL,
  ISBN VARCHAR(25) NOT NULL,
  id_imagen VARCHAR(45),
  Categoria_idCategoria INT NOT NULL,
  PRIMARY KEY (idLibro),
  UNIQUE INDEX ISBN_UNIQUE (ISBN ASC) ,
  INDEX id_imagen_UNIQUE (id_imagen ASC) ,
  INDEX fk_Libro_Categoria1_idx (Categoria_idCategoria ASC) )
ENGINE = InnoDB, CHARSET=latin1;


-- -----------------------------------------------------
-- Table Prestamo
-- -----------------------------------------------------
DROP TABLE IF EXISTS Prestamo ;

CREATE TABLE IF NOT EXISTS Prestamo (
  idPrestamo INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  Usuario_idUsuario INT NOT NULL,
  PRIMARY KEY (idPrestamo),
  INDEX fk_Prestamo_Usuario1_idx (Usuario_idUsuario ASC) )
ENGINE = InnoDB, CHARSET=latin1;


-- -----------------------------------------------------
-- Table detallePrestamo
-- -----------------------------------------------------
DROP TABLE IF EXISTS detallePrestamo;

CREATE TABLE IF NOT EXISTS detallePrestamo (
  id_detallePrestamo INT NOT NULL AUTO_INCREMENT,
  fecha_entrega DATE NOT NULL,
  fecha_devolucion DATE,
  Prestamo_idPrestamo INT NOT NULL,
  Libro_idLibro INT NOT NULL,
  PRIMARY KEY (id_detallePrestamo),
  INDEX fk_detallePrestamo_Prestamo1_idx (Prestamo_idPrestamo ASC),
  INDEX fk_detallePrestamo_Libro1_idx (Libro_idLibro ASC) )
ENGINE = InnoDB, CHARSET=latin1;


insert into Categoria(idCategoria, nombre) values (1, 'Ingenieria');
insert into Categoria(idCategoria, nombre) values (2, 'Ciencias');
insert into Categoria(idCategoria, nombre) values (3, 'Desarrollo personal');

insert into Usuario(correo, contrasena, privilegio) values('leonardo.vasquez@utec.edu.pe', 'leonardo', 'admin');
insert into Usuario(correo, contrasena, privilegio) values('leoandre987@gmail.com', 'leonardo', 'usuario');
insert into Usuario(correo, contrasena, privilegio) values('apll@gmail.com', 'alex', 'usuario');


insert into libro (nombre, autor, anio, edicion, ISBN, Categoria_idCategoria) values ('Clean Architecture', 'Robert C. Martin', '2018', 'Tercera', '9780134494166', '1');
insert into libro (nombre, autor, anio, edicion, ISBN, Categoria_idCategoria) values ('Cloud Computing', 'Nayan Ruparelia', '2016', 'Primera', '9780262529099', 1);
insert into libro (nombre, autor, anio, edicion, ISBN, Categoria_idCategoria) values ('Introduction to Embedded Systems', 'Manuel Jimenez', '2014', 'Primera', '9781461431428', 1);
insert into libro (nombre, autor, anio, edicion, ISBN, Categoria_idCategoria) values ('Tratamiento digital de señales', 'John G. Proakis', '2007', 'Primera', '9788483223475', 1);
insert into libro (nombre, autor, anio, edicion, ISBN, Categoria_idCategoria) values ('Computer Organization and Design', 'David A. Patterson', '2014', 'Quinta', '9780124077263', 1);


INSERT INTO prestamo(fecha, Usuario_idUsuario) values('2021-12-08', 2);
INSERT INTO detallePrestamo(fecha_entrega, fecha_devolucion, Prestamo_idPrestamo, Libro_idLibro) values('2021-12-11', '2021-12-12', 4, 1);

INSERT INTO prestamo(fecha, Usuario_idUsuario) values('2021-12-09', 2);
INSERT INTO detallePrestamo(fecha_entrega, Prestamo_idPrestamo, Libro_idLibro) values('2021-12-12', 5, 2);
INSERT INTO detallePrestamo(fecha_entrega, Prestamo_idPrestamo, Libro_idLibro) values('2021-12-12', 5, 4);

INSERT INTO prestamo(fecha, Usuario_idUsuario) values('2021-12-12', 2);
INSERT INTO detallePrestamo(fecha_entrega, Prestamo_idPrestamo, Libro_idLibro) values('2021-12-15', 6, 5);

INSERT INTO prestamo(fecha, Usuario_idUsuario) values('2021-12-13', 3);
INSERT INTO detallePrestamo(fecha_entrega, Prestamo_idPrestamo, Libro_idLibro) values('2021-12-16', 7, 2);