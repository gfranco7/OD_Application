from auth_manager import AuthManager
from OD_manager import OneDriveManager, DriveItem  # Asumo que DriveItem está allí
from typing import List

class OneDriveNavigator:
    def __init__(self):
        print(" Autenticando...")
        auth = AuthManager()
        self.token = auth.get_token()
        
        self.manager = OneDriveManager(self.token)
        self.history = []
        self.current_folder_id = None
        self.initialize()

    def initialize(self):
        drive_id, folder_id = self.manager.initialize_datacampus()
        self.current_folder_id = folder_id
        self.history.append(folder_id)

    def display_current_location(self):
        print(f"\n Ubicación actual: {self.current_folder_id}")

    def list_and_display_contents(self) -> List[DriveItem]:
        items = self.manager.list_folder_contents(self.current_folder_id)
        for i, item in enumerate(items):
            icon = "📁" if item.type == "folder" else "📄"
            print(f"{i + 1}. {icon} {item.name}")
        return items

    def navigate_to_item(self, items: List[DriveItem], selection: int) -> bool:
        if 0 <= selection < len(items):
            selected = items[selection]
            if selected.type == "folder":
                self.current_folder_id = selected.id
                self.history.append(selected.id)
                return True
        return False

    def go_back(self) -> bool:
        if len(self.history) > 1:
            self.history.pop()
            self.current_folder_id = self.history[-1]
            return True
        print("❗ Ya estás en la raíz.")
        return False

    def create_excel_interactive(self):
        filename = input("Nombre del archivo Excel: ")
        self.manager.create_excel_file(self.current_folder_id, filename)

    def read_excel_interactive(self, items: List[DriveItem]):
        selection = int(input("Número del archivo Excel a leer: ")) - 1
        file = items[selection]
        df = self.manager.read_excel_file(file.id)
        print(df)

    def edit_excel_interactive(self, items: List[DriveItem]):
        selection = int(input("Número del archivo Excel a editar: ")) - 1
        file = items[selection]
        df = self.manager.read_excel_file(file.id)

        print(" Mostrando datos actuales:")
        print(df)

        # Aquí podrías agregar una edición manual simulada o real
        df['Editado'] = 'Sí'
        self.manager.update_excel_file(file.id, df)

    def delete_item_interactive(self, items: List[DriveItem]):
        selection = int(input("Número del archivo o carpeta a eliminar: ")) - 1
        item = items[selection]
        self.manager.delete_item(item.id)

    def create_folder_interactive(self):
        folder_name = input("Nombre de la nueva carpeta: ")
        self.manager.create_folder(self.current_folder_id, folder_name)

    def run(self):
        while True:
            self.display_current_location()
            items = self.list_and_display_contents()

            print("\nOpciones:")
            print(" 0. Subir")
            print(" c. Crear carpeta")
            print(" e. Crear archivo Excel")
            print(" r. Leer archivo Excel")
            print(" a. Actualizar archivo Excel")
            print(" d. Eliminar archivo/carpeta")
            print(" q. Salir")

            choice = input("Seleccione opción o número de carpeta: ").strip().lower()

            if choice == "q":
                break
            elif choice == "0":
                self.go_back()
            elif choice == "c":
                self.create_folder_interactive()
            elif choice == "e":
                self.create_excel_interactive()
            elif choice == "r":
                self.read_excel_interactive(items)
            elif choice == "a":
                self.edit_excel_interactive(items)
            elif choice == "d":
                self.delete_item_interactive(items)
            elif choice.isdigit():
                idx = int(choice) - 1
                if not self.navigate_to_item(items, idx):
                    print("❌ No es una carpeta.")
            else:
                print("❌ Opción no válida.")

