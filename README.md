# Kobza

A free and open-source ESL course.

> ⚠️ **Pre-alpha**  
> Need to make pages with actual content.

## The Idea

Let's create a free and open-source English course to support teachers.

As an English teacher from Ukraine, the main obstacle to working independently has always been the lack of teaching materials. Even official private schools often purchase a single book to teach hundreds of students, which constitutes piracy. So-called "multimedia solutions" essentially offer interactive wrappers around regular page scans.

> Kobza is a Ukrainian musical instrument, a predecessor of Bandura.  
> The name should be fitting for a sound but humble project.

## Features and Goals

- [x] Parse JSON lessons into web pages
- [x] Interactive exercises
- [x] Vocabulary flashcards
- [x] Proper styling
- [ ] Warmup activities
- [ ] Interactive tests

## Ways to Help

- Contribute lesson materials to expand the coverage
- Help correct mistakes (I'm not a native speaker)
- Suggest code improvements
- Something else?..

## .colson

I aim to parse lessons from the most accessible and convenient format.

- Standard `Markdown` doesn't provide enough semantics to distinguish content.
- `JSON` is versatile but difficult to write from scratch or read without an admin panel.
- `YAML` doesn't handle inline Markdown well.

For now, I've developed my own [ColSON syntax](https://github.com/shushtain/colson-vscode) and [ColSON parser](https://github.com/shushtain/colson-pip). These handle the special files you might have spotted in the repository. They are essentially `.txt` files parsed line-by-line into Python objects, which are then converted into appropriate HTML elements using recipes in `parser.py`.

If you wish to help me create lessons, you can provide them in any format.

<!-- ## Resources -->
