# Trabalho Final - Sequência

## Introdução

Este repositório contém o trabalho final da disciplina de Engenharia de Software, que consiste no desenvolvimento de um programa distribuído para a disputa de partidas de Sequência na modalidade usuário contra usuário.

## Objetivo

Desenvolver um programa que suporte partidas de Sequência entre dois usuários, utilizando uma arquitetura cliente-servidor distribuída.

## Regras do Jogo

As regras do jogo Sequência podem ser encontradas no [site da Copag](https://copag.com.br/blog/detalhes/sequence).

## Arquitetura do Programa

O programa é baseado em uma arquitetura cliente-servidor distribuída, implementada em Python em conjunto com biblioteca [TKinter](https://docs.python.org/3/library/tkinter.html). Ele utiliza DOG como suporte para a execução distribuída.

## Premissas de Desenvolvimento

- O programa deve ser implementado em Python.
- O programa deve utilizar DOG (Distributed Objects in Python) como suporte para execução distribuída.
- Além do código-fonte, este repositório contém uma especificação de projeto baseada em UML (Unified Modeling Language), versão 2.

## Estrutura do Repositório

- `src/`: Contém o código-fonte do programa.
- `docs/`: Contém a documentação do projeto, incluindo a especificação UML.
- `README.md`: Este arquivo de documentação.

## Instalação e Execução

1. Clone este repositório:

    ```sh
    git clone https://github.com/vvc-git/engenharia-de-software.git
    cd engenharia-de-software
    ```

2. Crie um ambiente virtual e ative-o:

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4. Execute:

    ```sh
    python src/main.py
    ```

![secquencia-1](https://github.com/vvc-git/engenharia-de-software/assets/78426009/cb2215cb-e4e4-4286-8587-b9542e30c11c)
![sequencia-2](https://github.com/vvc-git/engenharia-de-software/assets/78426009/caa60cff-656f-4a4d-8067-f1964e9c5cb3)

# Final Project - Sequence

## Introduction

This repository contains the final project for the Software Engineering course, which involves developing a distributed program for playing Sequence games in a user-versus-user mode.

## Objective

Develop a program that supports Sequence games between two users, using a distributed client-server architecture.

## Game Rules

The rules of the Sequence game can be found on the [Copag website](https://copag.com.br/blog/detalhes/sequence).

## Program Architecture

The program is based on a distributed client-server architecture, implemented in Python together with the [TKinter](https://docs.python.org/3/library/tkinter.html) library. It uses DOG as support for distributed execution.

## Development Premises

- The program must be implemented in Python.
- The program must use DOG (Distributed Objects in Python) as support for distributed execution.
- In addition to the source code, this repository contains a project specification based on UML (Unified Modeling Language), version 2.

## Repository Structure

- `src/`: Contains the program's source code.
- `docs/`: Contains the project documentation, including the UML specification.
- `README.md`: This documentation file.

## Installation and Execution

1. Clone this repository:

    ```sh
    git clone https://github.com/vvc-git/engenharia-de-software.git
    cd engenharia-de-software
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Execute:

    ```sh
    python src/main.py
    ```
