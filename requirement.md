# Guitar Fret Trainer

I'd like you to build a CLI app in python that helps users learn guitar fret positions. This CLI app should be an interactive app. 

When entering the app, user will see a welcome message showing instruction. User could click either `Z` key or `X` key to run an exercise set, and could repeatly do so until user interrupts the program by running `Ctrl + C`.

When user click `Z` key (location exercise), the app should give a randomly sorted string of seven note (CDEFGAB). Each note in an exercise should only appear one. Here is the example output:

```
FGCADEB
```

When user click `X` key (inverse-location exercise), this app should give a randomly selected fret position (only the top 12 frets) on the six strings, when diagram attached. It's fine to have same fret position on the two strings (i.e. sample position with replacement).

Here is an example output for one string.
```
3 )   |   | * |   | . |   | . |   | . |   |   | : |
```
This is just a very rough illustration. You should use a better way (e.g. light blue color for select fret position, and gray color for other fret position, and you could use better symbol than `*`, `.`, `:` to indicate the fret position). You should give six strings in one exercise (i.e. 6 lines output).