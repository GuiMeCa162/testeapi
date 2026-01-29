CREATE DATABASE db_vitrinepp;
USE db_vitrinepp;

CREATE TABLE tb_marca(
    mar_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    mar_nome VARCHAR(40) NOT NULL,
    mar_caminho_foto PATH,
    mar_descricao TEXT,
    mar_caminho_banner PATH
);

CREATE TABLE tb_email(
    ema_id INT PRIMARY KEY NOT NULL AUTOO_INCREMENT,
    ema_endereco VARCHAR(40),

    ema_mar_id INT NOT NULL,
    FOREIGN KEY(ema_mar_id)
    REFERENCES tb_marca(mar_id)
);

CREATE TABLE tb_telefone(
    tel_id INT PRIMARY KEY NOT NULL AUTOO_INCREMENT,
    tel_numero VARCHAR(40),

    tel_mar_id INT NOT NULL,
    FOREIGN KEY(tel_mar_id)
    REFERENCES tb_marca(mar_id)
);

CREATE TABLE tb_roupa(
    rou_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    rou_nome VARCHAR(40) NOT NULL,
    rou_descricao TEXT,
    rou_preco FLOAT NOT NULL,
    rou_destaque BOOLEAN,
    rou_caminho_imagem PATH,
    rou_n_visualizacoes INT,
    rou_n_curtidas INT

    rou_mar_id INT NOT NULL,
    FOREIGN KEY(rou_mar_id)
    REFERENCES tb_marca(mar_id)
);

CREATE TABLE tb_tamanho(
    tam_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    tam_nome ENUM('PP', 'P', 'M', 'G', 'GG', 'XG') NOT NULL,

    tam_rou_id INT NOT NULL
    FOREIGN KEY(tam_rou_id)
    REFERENCES tb_roupa(rou_id)
);

CREATE TABLE tb_imagem_extra(
    ima_ext_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    ima_ext_caminho PATH NOT NULL,

    ima_ext_rou_id INT NOT NULL,
    FOREIGN KEY(ima_ext_rou_id)
    REFERENCES tb_roupa(rou_id)
);