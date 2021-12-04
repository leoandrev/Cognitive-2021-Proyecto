-- -----------------------------------------------------
-- Table Usuario
-- -----------------------------------------------------
DROP TABLE IF EXISTS Usuario ;

CREATE TABLE IF NOT EXISTS Usuario (
  idUsuario INT NOT NULL AUTO_INCREMENT,
  correo VARCHAR(45) NOT NULL,
  nickname VARCHAR(10) NULL,
  contrasena VARCHAR(15) NOT NULL,
  privilegio VARCHAR(7) NOT NULL,
  PRIMARY KEY (idUsuario),
  UNIQUE INDEX usuario_UNIQUE (nickname ASC) VISIBLE,
  UNIQUE INDEX correo_UNIQUE (correo ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table Categoria
-- -----------------------------------------------------
DROP TABLE IF EXISTS Categoria;

CREATE TABLE IF NOT EXISTS Categoria (
  idCategoria INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(20) NOT NULL,
  PRIMARY KEY (idCategoria),
  UNIQUE INDEX Categoriacol_UNIQUE (nombre ASC) VISIBLE)
ENGINE = InnoDB;


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
  id_imagen VARCHAR(45) NOT NULL,
  Categoria_idCategoria INT NOT NULL,
  PRIMARY KEY (idLibro),
  UNIQUE INDEX ISBN_UNIQUE (ISBN ASC) VISIBLE,
  UNIQUE INDEX id_imagen_UNIQUE (id_imagen ASC) VISIBLE,
  INDEX fk_Libro_Categoria1_idx (Categoria_idCategoria ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table Prestamo
-- -----------------------------------------------------
DROP TABLE IF EXISTS Prestamo ;

CREATE TABLE IF NOT EXISTS Prestamo (
  idPrestamo INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  Usuario_idUsuario INT NOT NULL,
  PRIMARY KEY (idPrestamo),
  INDEX fk_Prestamo_Usuario1_idx (Usuario_idUsuario ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table detallePrestamo
-- -----------------------------------------------------
DROP TABLE IF EXISTS detallePrestamo;

CREATE TABLE IF NOT EXISTS detallePrestamo (
  id_detallePrestamo INT NOT NULL AUTO_INCREMENT,
  fecha_devolucion DATE NOT NULL,
  fecha_entrega DATE NOT NULL,
  Prestamo_idPrestamo INT NOT NULL,
  Libro_idLibro INT NOT NULL,
  PRIMARY KEY (id_detallePrestamo),
  INDEX fk_detallePrestamo_Prestamo1_idx (Prestamo_idPrestamo ASC) VISIBLE,
  INDEX fk_detallePrestamo_Libro1_idx (Libro_idLibro ASC) VISIBLE)
ENGINE = InnoDB;