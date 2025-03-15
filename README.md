# Kobza

Free and open source English (as a second language) course

> ⚠️ **Pre-alpha**  
> There are no actual lessons yet, just a functioning `JSON → HTML` parser.

## The idea

Let's make a free and open source English course happen, to make it easier for teachers.

As an English teacher from Ukraine, the only thing that always stopped me from working independently is the absence of my own teaching materials. Even official private schools often buy a single book to teach hundreds of students, which is pirating. So-called "multimedia solutions" basically offer interactive wrappers on top of regular page scans.

> 💅 Kobza is a Ukrainian musical instrument, a prototype of Bandura.

## Features and goals

- [x] Parse JSON lessons into web pages.
- [x] Interactive exercises.
- [ ] Proper styling.
- [ ] Vocabulary flashcards.
- [ ] Interactive tests.
- [ ] Warmup activities.

## Ways to help

- Supply your own lesson materials to expand the coverage.
- Help fix mistakes (I'm only a self-taught C1 enjoyer, so...)
- Point out where my ~~shitty~~ code is especially bad.
- Maybe something else?

## .columnson

I would prefer to parse lessons from the most accessible and convenient format.

- General `Markdown` doesn't provide enough semantics to distinguish content.
- `JSON` is limitless but a pain to write from scratch or read, unless there is an admin panel.

For now, I've made my own [ColumnSON](https://github.com/shushtain/columnson) syntax, inspired by Python. That's what those strange files are. Essentally, they are `.txt` files parsed line-by-line into Python dictionaries which then are parsed into appropriate html elements.

<!-- ## Resources -->
