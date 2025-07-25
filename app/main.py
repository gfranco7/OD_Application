from app.one_drive.OD_manager import OneDriveManager, DriveItem
import pandas as pd
from typing import List, Optional
from app.auth.auth_manager import AuthManager
from app.one_drive.OD_manager import OneDriveManager

class OneDriveNavigator:

    def __init__(self):
        print(" Autenticando...")
        auth = AuthManager()
        self.token = auth.get_token()
        self.current_path = ["datacampus"]
        self.navigation_history = []
        self.manager = OneDriveManager(self.token)
        self.history = []
        self.current_folder_id = None
        self.initialize()

    def initialize(self):
        print("Inicializando OneDrive Manager...")
        drive_id, root_id = self.manager.initialize_datacampus()
        self.current_folder_id = root_id
        print(" Listo para operar en datacampus\n")

    def display_current_location(self):
        """Mostrar ubicación actual"""
        path_str = " > ".join(self.current_path)
        print(f" Ubicación actual: {path_str}")

    def list_and_display_contents(self) -> List[DriveItem]:
        """Listar y mostrar contenido de la carpeta actual"""
        try:
            items = self.manager.list_folder_contents(self.current_folder_id)
            
            if not items:
                print(" Carpeta vacía")
                return []

            print(f"\n Contenido de la carpeta ({len(items)} elementos):")
            print("-" * 60)
            
            folders = [item for item in items if item.type == 'folder']
            files = [item for item in items if item.type == 'file']

            if folders:
                print(" CARPETAS:")
                for i, folder in enumerate(folders, 1):
                    print(f"  {i}.  {folder.name}")
                print()

            if files:
                print(" ARCHIVOS:")
                folder_count = len(folders)
                for i, file in enumerate(files, folder_count + 1):
                    size_mb = file.size / (1024 * 1024) if file.size > 0 else 0
                    print(f"  {i}. {file.name} ({size_mb:.2f} MB)")
                print()

            return items
            
        except Exception as e:
            print(f" Error al listar contenido: {e}")
            return []

    def navigate_to_item(self, items: List[DriveItem], selection: int) -> bool:
        """Navegar a un elemento seleccionado"""
        try:
            if 1 <= selection <= len(items):
                selected_item = items[selection - 1]
                
                if selected_item.type == 'folder':
                    # Guardar ubicación actual para navegación
                    self.navigation_history.append((self.current_folder_id, self.current_path.copy()))
                    
                    # Navegar a la carpeta
                    self.current_folder_id = selected_item.id
                    self.current_path.append(selected_item.name)
                    
                    print(f" Navegando a: {selected_item.name}")
                    return True
                else:
                    print(f" Has seleccionado el archivo: {selected_item.name}")
                    return False
            else:
                print(" Selección inválida")
                return False
                
        except Exception as e:
            print(f"Error en navegación: {e}")
            return False

    def go_back(self) -> bool:
        if self.navigation_history:
            self.current_folder_id, self.current_path = self.navigation_history.pop()
            print("  Regresando a carpeta anterior")
            return True
        else:
            print(" Ya estás en la carpeta raíz")
            return False

    def create_excel_interactive(self):
        """Crear archivo Excel interactivamente"""
        try:
            filename = input(" Nombre del archivo Excel (sin extensión): ").strip()
            if not filename:
                print(" Nombre de archivo no válido")
                return

            print("\n ¿Deseas crear un archivo con datos personalizados? (s/n): ", end="")
            custom_data = input().strip().lower() == 's'
            
            data = None
            if custom_data:
                print(" Ingresa datos separados por comas (ejemplo: col1,col2,col3):")
                columns = input("Nombres de columnas: ").split(',')
                columns = [col.strip() for col in columns if col.strip()]
                
                if columns:
                    data_dict = {}
                    for col in columns:
                        values_str = input(f"Valores para '{col}' (separados por coma): ")
                        values = [val.strip() for val in values_str.split(',') if val.strip()]
                        data_dict[col] = values
                    
                    data = pd.DataFrame(data_dict)

            result = self.manager.create_excel_file(self.current_folder_id, filename, data)
            print(f" Archivo creado con ID: {result['id'][:8]}...")
            
        except Exception as e:
            print(f" Error al crear archivo: {e}")

    def read_excel_interactive(self, items: List[DriveItem]):
        """Leer archivo Excel interactivamente"""
        try:
            excel_files = [item for item in items if item.type == 'file' and item.name.endswith('.xlsx')]
            
            if not excel_files:
                print(" No hay archivos Excel en esta carpeta")
                return
            
            print("\n Archivos Excel disponibles:")
            for i, file in enumerate(excel_files, 1):
                print(f"  {i}. {file.name}")
            
            try:
                selection = int(input("\nSelecciona archivo a leer (número): ")) - 1
                if 0 <= selection < len(excel_files):
                    selected_file = excel_files[selection]
                    df = self.manager.read_excel_file(selected_file.id)
                    
                    print(f"\n Contenido de '{selected_file.name}':")
                    print("-" * 50)
                    print(df.to_string(max_rows=10, max_cols=5))
                    
                    if len(df) > 10:
                        print(f"\n... y {len(df) - 10} filas más")
                        
                else:
                    print(" Selección inválida")
                    
            except ValueError:
                print(" Debes ingresar un número")
                
        except Exception as e:
            print(f" Error al leer archivo: {e}")

    def edit_excel_interactive(self, items: List[DriveItem]):
        """Editar archivo Excel interactivamente"""
        try:
            excel_files = [item for item in items if item.type == 'file' and item.name.endswith('.xlsx')]
            
            if not excel_files:
                print(" No hay archivos Excel en esta carpeta")
                return
            
            print("\n  Archivos Excel disponibles para editar:")
            for i, file in enumerate(excel_files, 1):
                print(f"  {i}. {file.name}")
            
            try:
                selection = int(input("\nSelecciona archivo a editar (número): ")) - 1
                if 0 <= selection < len(excel_files):
                    selected_file = excel_files[selection]
                    
                    # Leer archivo actual
                    df = self.manager.read_excel_file(selected_file.id)
                    print(f"\nContenido actual de '{selected_file.name}':")
                    print(df.to_string())
                    
                    # Opciones de edición
                    print("\n  Opciones de edición:")
                    print("1. Agregar nueva fila")
                    print("2. Modificar valor específico")
                    print("3. Agregar nueva columna")
                    print("4. Eliminar fila")
                    
                    edit_option = input("Selecciona opción de edición: ").strip()
                    
                    if edit_option == "1":
                        # Agregar nueva fila
                        new_row = {}
                        for col in df.columns:
                            value = input(f"Valor para '{col}': ")
                            # Intentar convertir a número si es posible
                            try:
                                new_row[col] = float(value) if '.' in value else int(value)
                            except ValueError:
                                new_row[col] = value
                        
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        
                    elif edit_option == "2":
                        # Modificar valor específico
                        try:
                            row_idx = int(input(f"Índice de fila (0-{len(df)-1}): "))
                            col_name = input(f"Nombre de columna {list(df.columns)}: ")
                            
                            if col_name in df.columns and 0 <= row_idx < len(df):
                                current_value = df.iloc[row_idx][col_name]
                                print(f"Valor actual: {current_value}")
                                new_value = input("Nuevo valor: ")
                                
                                # Intentar mantener el tipo de dato
                                try:
                                    if isinstance(current_value, (int, float)):
                                        new_value = float(new_value) if '.' in new_value else int(new_value)
                                except ValueError:
                                    pass  # Mantener como string
                                
                                df.iloc[row_idx, df.columns.get_loc(col_name)] = new_value
                            else:
                                print(" Índice o columna inválidos")
                                return
                        except ValueError:
                            print(" Índice debe ser un número")
                            return
                    
                    elif edit_option == "3":
                        # Agregar nueva columna
                        col_name = input("Nombre de la nueva columna: ")
                        default_value = input("Valor por defecto para la columna: ")
                        
                        # Intentar convertir a número si es posible
                        try:
                            default_value = float(default_value) if '.' in default_value else int(default_value)
                        except ValueError:
                            pass  # Mantener como string
                        
                        df[col_name] = default_value
                    
                    elif edit_option == "4":
                        # Eliminar fila
                        try:
                            row_idx = int(input(f"Índice de fila a eliminar (0-{len(df)-1}): "))
                            if 0 <= row_idx < len(df):
                                df = df.drop(df.index[row_idx]).reset_index(drop=True)
                            else:
                                print(" Índice inválido")
                                return
                        except ValueError:
                            print(" Índice debe ser un número")
                            return
                    
                    else:
                        print(" Opción inválida")
                        return
                    
                    # Actualizar archivo
                    self.manager.update_excel_file(selected_file.id, df)
                    print(f"Archivo '{selected_file.name}' actualizado exitosamente")
                    
                else:
                    print(" Selección inválida")
                    
            except ValueError:
                print(" Debes ingresar un número")
                
        except Exception as e:
            print(f" Error al editar archivo: {e}")

    def delete_item_interactive(self, items: List[DriveItem]):
        """Eliminar elemento interactivamente"""
        try:
            if not items:
                print(" No hay elementos para eliminar")
                return
            
            print("\n  Elementos disponibles para eliminar:")
            for i, item in enumerate(items, 1):
                icon = "" if item.type == 'folder' else " "
                print(f"  {i}. {icon} {item.name}")
            
            try:
                selection = int(input("\nSelecciona elemento a eliminar (número): ")) - 1
                if 0 <= selection < len(items):
                    selected_item = items[selection]
                    
                    # Confirmación
                    confirm = input(f" ¿Estás seguro de eliminar '{selected_item.name}'? (s/N): ").strip().lower()
                    if confirm == 's':
                        self.manager.delete_item(selected_item.id)
                        print(f" '{selected_item.name}' eliminado exitosamente")
                    else:
                        print(" Eliminación cancelada")
                else:
                    print(" Selección inválida")
                    
            except ValueError:
                print(" Debes ingresar un número")
                
        except Exception as e:
            print(f" Error al eliminar elemento: {e}")

    def create_folder_interactive(self):
        """Crear carpeta interactivamente"""
        try:
            folder_name = input(" Nombre de la nueva carpeta: ").strip()
            if not folder_name:
                print(" Nombre de carpeta no válido")
                return
            
            result = self.manager.create_folder(self.current_folder_id, folder_name)
            print(f" Carpeta '{folder_name}' creada exitosamente")
            
        except Exception as e:
            print(f" Error al crear carpeta: {e}")

    def run(self):
        """Ejecutar el navegador interactivo"""
        self.initialize()
        
        while True:
            print("\n" + "="*60)
            self.display_current_location()
            print("="*60)
            
            # Listar contenido actual
            current_items = self.list_and_display_contents()
            

            print("\n OPCIONES DISPONIBLES:")
            print("1.  Navegar a carpeta/archivo (seleccionar número)")
            print("2.   Regresar a carpeta anterior")
            print("3.  Crear archivo Excel")
            print("4.  Leer archivo Excel")
            print("5.   Editar archivo Excel")
            print("6.  Eliminar elemento")
            print("7.  Crear nueva carpeta")
            print("8.  Actualizar vista")
            print("9.  Salir")
            
            try:
                option = input("\n Selecciona una opción: ").strip()
                
                if option == "1":
                    if current_items:
                        try:
                            item_num = int(input("Número de elemento: "))
                            self.navigate_to_item(current_items, item_num)
                        except ValueError:
                            print(" Debes ingresar un número válido")
                    else:
                        print(" No hay elementos para navegar")
                
                elif option == "2":
                    self.go_back()
                
                elif option == "3":
                    self.create_excel_interactive()
                
                elif option == "4":
                    self.read_excel_interactive(current_items)
                
                elif option == "5":
                    self.edit_excel_interactive(current_items)
                
                elif option == "6":
                    self.delete_item_interactive(current_items)
                
                elif option == "7":
                    self.create_folder_interactive()
                
                elif option == "8":
                    print(" Actualizando vista...")
                    continue
                
                elif option == "9":
                    print(" ¡Hasta luego!")
                    break
                
                else:
                    print(" Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n ¡Hasta luego!")
                break
            except Exception as e:
                print(f" Error inesperado: {e}")


def main():
    print(" OneDrive Manager - Sistema de Navegación CRUD")
    print("=" * 50)
    
    navigator = OneDriveNavigator()
    navigator.run()

if __name__ == "__main__":
    main()