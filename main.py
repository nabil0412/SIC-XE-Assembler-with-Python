from assembler import Assembler


def main():

    assembler = Assembler()
    try:
        assembler.assemble()
        print("Assembly completed successfully!")
    except Exception as e:
        print(f"Error during assembly: {str(e)}")



if __name__ == "__main__":
    exit(main())