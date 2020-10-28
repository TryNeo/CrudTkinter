drop database if exists crudTk;
create database if not exists crudTk;
use crudTK;

create table usuario(
id_usuario int auto_increment,
email varchar(50),
username varchar(50),
password TEXT,
primary key(id_usuario));

create table categoria(
id_categoria int auto_increment,
nombre varchar(50),
descripcion TEXT,
primary key (id_categoria));

create table producto(
id_producto int auto_increment,
nombre varchar(50),
descripcion TEXT,
cantidad int,
precio double,
categoria int,
primary key (id_producto));

ALTER TABLE producto ADD constraint fk_categoria foreign key (categoria) references categoria(id_categoria);

