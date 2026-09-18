# Car Showroom System

A small console project that practices **everything** from the `AI_Engineering` Python notebooks.

## How to run

```bash
cd Car_Showroom_System
python main.py
```

On Windows, if `python` is not found, use:

```bash
py -3 main.py
```

Then choose options `1`–`9` from the menu.

## Menu features

| # | Feature | What you practice |
| --- | --------- | ------------------- |
| 1 | Add car | `input()`, casting, OOP inheritance, `@property` validation |
| 2 | View all cars | loops, polymorphism, `__str__`, sets (unique brands) |
| 3 | Search / filter | `filter` + lambda |
| 4 | Sell car | custom exceptions, dict sales records |
| 5 | Sales report | `map`/`sum`, sets, dicts |
| 6 | Save inventory | file I/O with `with open`, JSON write |
| 7 | Load inventory | `FileNotFoundError`, try/except/else/finally |
| 8 | Merge demo | `__add__`, `__len__` |
| 9 | Exit | while-loop control |

## Project layout

```text
Car_Showroom_System/
├── main.py                 # menu loop (entry point)
├── models/
│   ├── car.py              # Car, ElectricCar, PetrolCar
│   ├── customer.py         # Customer
│   └── showroom.py         # Showroom inventory + sales
├── utils/
│   ├── exceptions.py       # InvalidPriceError, CarNotFoundError, ...
│   ├── file_handler.py     # save / load inventory.json
│   └── helpers.py          # filter_by_brand, total_price, ...
└── data/
    └── inventory.json      # created when you choose Save
```

## Learning map (notebook → project)

| Notebook topic | Where it shows up |
| ---------------- | ------------------- |
| `python_intro` / `type_conversion` | Variables, `int()` / `float()` on menu input |
| `loops` | `while` menu; `for` over cars |
| `data_structures` | list of cars, tuple `specs`, set of brands, sales `dict` |
| `functions` | helpers; lambda with `map` / `filter` |
| `python_modules` | packages `models` and `utils` imported from `main.py` |
| `read_and_write_to_files_in_python` | `save_inventory` / `load_inventory` |
| `exceptions` | custom errors + try/except/else/finally |
| `oop` | classes, inheritance, override, `@property`, polymorphism |
| `python_special_methods` | `__str__`, `__len__`, `__add__` on `Showroom` |

## Quick tip

On first run the app seeds 4 sample cars. Try **View all cars**, then **Sell car**, then **Save inventory**. Restart and use **Load inventory** to see file I/O working.
