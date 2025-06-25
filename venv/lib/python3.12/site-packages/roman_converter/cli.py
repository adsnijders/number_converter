# Import modules
import typer
import re
import numpy as np

# Initialize app
app = typer.Typer(help="Convert numerals between Roman and Arabic numeral systems")

# Define Roman to Arabic mapping
rom_to_ar = {
    "i": 1,
    "iv": 4,
    "v": 5,
    "ix": 9,
    "x": 10,
    "xl": 40,
    "l": 50,
    "xc": 90,
    "c": 100,
    "cd": 400,
    "d": 500,
    "cm": 900,
    "m": 1000,
}

# Define Arabic to Roman mapping
ar_to_rom = {ar_nr: rom_nr for rom_nr, ar_nr in rom_to_ar.items()}

# Define a function to validate the Roman input
def val_rom_inp(rom_inp: str) -> None:
    """
    Validate the input for rom_to_ar_conv
    """
    # The input must be a string
    if not isinstance(rom_inp, str):
        raise typer.BadParameter("Input must be a string")
    
    # Convert the input to lowercase
    rom_inp = rom_inp.lower()
    
    # Reject more than 3 of the same numeral in a row
    if re.search(r"(i{4,}|x{4,}|c{4,}|m{4,})", rom_inp):
        raise typer.BadParameter("Invalid Roman numeral: cannot repeat the same numeral for more than three times")
    
    # Allow only valid characters
    if not re.fullmatch(r"[ivxlcdm]+", rom_inp):
        raise typer.BadParameter("Input contains invalid Roman numeral")
    
# Define a function to validate the Arabic input
def val_ar_inp(ar_inp: str | int) -> None:
    """
    Validate the input for ar_to_rom_conv
    """
    # The input must be an integer or a string convertible to an integer
    try:
        ar_inp = int(ar_inp)
    except ValueError:
        raise typer.BadParameter("Input must be an integer or a string convertible to an integer")
    
    # inp_nr cannot be negative
    if ar_inp <= 0:
        typer.echo("Roman numerals must be positive integers")
        raise typer.Exit(code=1)
    
    return ar_inp
    
# Define a function for converting Roman numerals to Arabic numbers
@app.command("rom-to-ar")
def rom_to_ar_conv(
    inp_nr: str=typer.Argument(..., help='The Roman numeral to convert (e.g., "XI")')) -> str:
    """
    Convert a Roman numeral to an Arabic number
    """
    # Validate the input
    val_rom_inp(inp_nr)

    # Strip input and convert to lowercase
    inp_nr = inp_nr.lower().strip()

    # Define tot indicating the total sum
    tot = 0

    # Define idx indicating the index of the analyzed number
    idx = 0

    # While idx is smaller than the length of the input number the algorithm should continue
    while idx < len(inp_nr):
        # Define the rest of the number that should be analyzed
        check = inp_nr[idx:]
        
        # Create a list of all the possible roman numbers that the analyzed number could start with 
        finds = [re.findall(rf"^{key}", check)[0] for key in rom_to_ar.keys() if len(re.findall(rf"^{key}", check)) > 0]
        
        # Create a list of all the conversions following from list "finds"
        converts = [rom_to_ar[find] for find in finds]

        # Find the index of the highest conversion
        max_find_idx = converts.index(max(converts))
        
        # Add the highest conversion to "tot"
        tot += converts[max_find_idx]

        # Add the length of the roman number to "idx"
        idx += len(finds[max_find_idx])

    # Print result
    typer.echo(f"Arabic number: {tot}")

# Define a function for converting Arabic numbers to Roman numerals
@app.command("ar-to-rom")
def ar_to_rom_conv(inp_nr: int=typer.Argument(..., help="The Arabic numeral to convert (e.g., 44)")) -> str:
    """
    Convert an Arabic number to a Roman numeral
    """
    # Validate the input
    inp_nr = val_ar_inp(inp_nr)

    # Define the remainder
    remain = inp_nr

    # Define the roman numeral
    rom_nr = ""

    # While "substr" is smaller than the input number, the algorithm should continue
    while remain > 0:
        # Define a list of all possible substractions
        substr_list = [key for key in ar_to_rom if remain - key >= 0]

        # Define the maximal possible substraction
        max_substr = max(substr_list)

        # Update the remainder
        remain -= max_substr

        # Update the roman numeral
        rom_nr += ar_to_rom[max_substr]
    
    # Print result
    typer.echo(f"Roman numeral: {rom_nr.upper()}")

if __name__ == "__main__":
    app()