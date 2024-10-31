# Welcome to the FanSTATIC Site Generator

This project allows you to generate html formatted website from markdown files

## How to setup

- Make sure you have python 3 installed
- Check if you have your md cheat sheet with you, can always refer to [markdown guide](https://www.markdownguide.org/cheat-sheet/)
- Keep in mind this is a initial version and support only the basic stuff

## How to run

- Clone the repo locally
- Replace the files inside folder content with the ones you want to be converted(the program will convert recursively so you can nest folders)
- Add any static content inside the folder static(this will be copied in the same structure to the public folder generated
- Make any update you want to the template.html file in the root, this will allow you to make your site have your style all over it!
- Finally time to make it shine, run `sh main.sh` in your terminal, it should convert all your markdown files and start the server at port 8888

## Improvements

- Convert `[ ]` into checkbox
- Allow nested conversions like **This is a bold sentence but also has *italic* word in it** or the inverse *Italic sentence with some **bold** word in it*

# Thanks to

- Boot.dev for pointing the direction on how to build this

