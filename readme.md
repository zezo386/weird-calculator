# Weird Calculator

## Tech stack

this app is made using python and the gui is made using tkinter

## Purpose

help me with my 9th grade (egyptian) math algebra since our 5th and 6th lessons are on the operations on real fractions with variables of all kinds of degrees

## Features

### Polynomials

the algorithm can handle basic terms, Polynomials, products of polynomails and also fractions

it can also handle basic operations (+ - * /) between all of them but requires int coefficients so no decimals here

it can parse almost anything

### simplifying polynomials

the algorithm also has a way to simplify polynomials by adding like-terms together

### factoring by gcf

the algorithm can also factorize by getting out the gcf and can determine if there even is a gcf or not

### factoring a trinomial

the algorithm can also factorize trinomials like x^2 + 2x + 1 into two brackets and can also factor trinomials where a is greater than 1

### difference between two squares

the algorithm can also detect the difference between two squares and factor them into two brackets (binomials)

### sum and difference between cubes

the algorithm can also detect the sum and difference between two cubes and factor them into a small and a large bracket (binomial and trinomial)

### factoring by grouping

the algorithm also tries to factor by grouping by using all possile combinations between all terms of the polynomial

### factorizing the polynomials

to factorize polynomials the algorithm tries all methods above one after the other repeatedly until the polynomial cant get factored more to give the complete factorization of the polynomial

## Fractions

the main part of this calculator is to calculate fractions

each fraction is made up of a numerator and a denomenator

### Multiplication and division

when making a fraction to multiply we multiply the numerators together and denomenators together into a single fraction

while division is just multiplying the numerators of the 2nd to the denomenators of the 1st and the denomenators of the 2nd to the numerators of the 1st

### Addition

addition and subtraction differ between if the denomenator is the same or not

if they both have the same denomenator we just add the two numerators

if not we use the cross method and add the results once the denomenators are the same

## GUI

the gui is made using tkinter and only has a small input field to enter the expression

a text field to show the result/ error

a drop down menu to choose the function you want to use

## Math parts

come to this section if you dont understand something in the math itself

i am here to help :)

### how to simplify polynomials

to simplify a polynomial you add up the coefficients of like terms

for example in this polynomial

3x^2 + 5x - 7 - 2x + 6x^2

we see that 5x and -2x are like terms since they have the same variable with the same degree (power) so we add up the coefficients to get 3x

and 3x^2 + 6x^2 are like terms since they have the same variable with the same degree (power) so we add up the coefficients to get 9x^2

while -7 does not have any other like terms

so the final polynomial is

9x^2 + 3x - 7

### GCF

a gcf is the greatest common factor so between for example 8x and 12x^2 the greatest common factor is 4x even though other factors exist like 4 or x or 2x the greatest common factor between these 2 terms is 4x

### binomial

a binomial is a 2 term polynomial that is expressed like this

mx + b

### trinomials

a trinomial is a 3 term polynomial that is expressed like this

ax^2 + bx + c

where c is the constant term

to solve it normally you factorize it into two brackets in the sense of

(x1 + i) * (x2 + j)

and i*j has to equal c and i + j has to equal b where a = 1

for a != 1 we use a way called the AC method

you can search for it since it has alot of explanation

### how to difference between two squares

when having a binomial in this form

x^2 - y^2

so that we can take the sqrt of the first and the 2nd term the middle term cancels out so its factorization is

(x + y) * (x - y)

if we reexpand it we get

x^2 - xy + xy - y^2

and the -xy and +xy cancel out

### how to difference and sum between two cubes

when having a binomial in this form

x^3 + y^3

so that we can take the sqrt of the first and the 2nd term the middle terms cancels out so its factorization is

(x + y) * (x^2 - xy + y^2)

if we reexpand it we get

x^3 - x^2y + x^2y - xy^2 + xy^2 + y^2

and the -x^2y and +x^2y cancel out

and the -xy^2 and the +xy^2 also cancel out

the difference works in the same way we just flip the signs in the middle so the factorization of

x^3 - y^3 =

(x - y) * (x^2 + xy + y^2)

### cross method

we use the cross method to make the denomenators equal while making the fraction still the same after removing common factors

if we have fractions a/b + c/d

we make it ad + cb / bd

## AI statment

this project didnt use any ai in the algorithms itself it only made tests to check for quicker checks since the deadline was in a day

the only ai code in this project is about half the gui code since i was in hurry to finish this project

## Contributers

this project is made entirly by **ZIAD ELHUSINY**

the **GOAT OF PROGRAMMING**
