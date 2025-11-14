
CREATE TABLE comicverse.editorial (
    id_editorial INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    fecha_fundacion DATE,
    sitio_web VARCHAR(255) UNIQUE
);

CREATE TABLE comicverse.comic (
    id_comic INT IDENTITY(1,1) PRIMARY KEY,
    num_comic INT,
    titulo VARCHAR(200) NOT NULL,
    id_editorial INT NOT NULL,
    id_autor INT NOT NULL,
    fecha_publicacion DATE
);

CREATE TABLE comicverse.autor (
    id_autor INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(200)
);

CREATE TABLE comicverse.cliente (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    email VARCHAR(200) UNIQUE,
);

CREATE TABLE comicverse.pedido (
    id_pedido INT IDENTITY(1,1) PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_pedido DATE,
    fecha_entrega DATE
);

CREATE TABLE comicverse.comics_pedidos (
    id_pedido INT NOT NULL,
    id_comic INT NOT NULL,
    cantidad_comics INT,
    estado VARCHAR(50)
);

ALTER TABLE comicverse.comic
ADD CONSTRAINT FK_comic_editorial
    FOREIGN KEY (id_editorial)
    REFERENCES comicverse.editorial(id_editorial);

ALTER TABLE comicverse.comic
ADD CONSTRAINT FK_comic_autor
    FOREIGN KEY (id_autor)
    REFERENCES comicverse.autor(id_autor);

ALTER TABLE comicverse.pedido
ADD CONSTRAINT FK_pedido_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES comicverse.cliente(id_cliente);

    ALTER TABLE comicverse.comics_pedidos
ADD CONSTRAINT FK_comicspedidos_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES comicverse.pedido(id_pedido);

ALTER TABLE comicverse.comics_pedidos
ADD CONSTRAINT FK_comicspedidos_comic
    FOREIGN KEY (id_comic)
    REFERENCES comicverse.comic(id_comic);

ALTER TABLE comicverse.autor
ADD CONSTRAINT emailunico UNIQUE (email);

ALTER TABLE comicverse.comics_pedidos
ADD CONSTRAINT PK_comics_pedidos
PRIMARY KEY (id_pedido, id_comic);
























