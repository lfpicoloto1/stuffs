import os
import shutil
import re


def update_help_md(root_directory):
    print(root_directory)
    for dirpath, dirnames, filenames in os.walk(root_directory):
        
        if 'help.md' in filenames:
            help_md_path = os.path.join(dirpath, 'help.md')
            last_folder_name = os.path.basename(dirpath)
            capitalized_folder_name = last_folder_name.capitalize()

            with open(help_md_path, 'r') as file:
                lines = file.readlines()

            if lines and lines[0].startswith('#'):
                old_title = lines[0].strip()
                new_title = f"# {capitalized_folder_name}\n"
                description = f"\n{old_title}\n" + "".join(lines[1:])
            else:
                new_title = f"# {capitalized_folder_name}\n"
                description = "".join(lines)

            with open(help_md_path, 'w') as file:
                file.write(new_title)
                file.write(description)

            print(f"Updated {help_md_path} with title '{capitalized_folder_name}'.")



def move_single_file_folders(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory, topdown=False):
        # Verifica se a pasta tem apenas um arquivo
        if len(filenames) == 1 and len(dirnames) == 0:
            file_to_move = filenames[0]
            source_path = os.path.join(dirpath, file_to_move)
            parent_dir = os.path.dirname(dirpath)
            new_file_name = os.path.basename(dirpath) + ".md"
            destination_path = os.path.join(parent_dir, new_file_name)
            
            # Move o arquivo para o diretório pai com o novo nome
            shutil.move(source_path, destination_path)
            
            # Remove a pasta vazia
            os.rmdir(dirpath)
            
            print(f"Moved {source_path} to {destination_path} and removed directory {dirpath}.")



def insert_sidebar_position(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        md_files = [f for f in filenames if f.endswith('.md')]
        if md_files:
            ordered_files = []
            unordered_files = []

            # Classifica os arquivos de acordo com as regras
            for md_file in md_files:
                if md_file == 'help.md':
                    ordered_files.append((md_file, 0))
                elif md_file == 'list.md':
                    ordered_files.append((md_file, 1))
                elif md_file == 'create.md':
                    ordered_files.append((md_file, 2))
                else:
                    unordered_files.append(md_file)

            # Ordena os arquivos restantes com índices subsequentes
            index = 3
            for md_file in unordered_files:
                ordered_files.append((md_file, index))
                index += 1

            # Atualiza cada arquivo com o índice apropriado
            for md_file, position in ordered_files:
                file_path = os.path.join(dirpath, md_file)
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Inserir o contador no início do arquivo
                new_lines = ["---\n", f"sidebar_position: {position}\n", "---\n"] + lines

                with open(file_path, 'w') as file:
                    file.writelines(new_lines)

                print(f"Updated {file_path} with sidebar_position: {position}")


def remove_hash_from_line_6(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                # Verifica se a linha 6 existe e começa com '#'
                if len(lines) >= 6 and lines[5].strip().startswith('#'):
                    # Remove o '#' e mantém o restante da linha
                    lines[5] = lines[5].lstrip('#').lstrip() + '\n'
                    
                    with open(file_path, 'w') as file:
                        file.writelines(lines)
                    
                    print(f"Updated {file_path}, modified line 6")


def format_mgc_commands(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                
                with open(file_path, 'r') as file:
                    content = file.read()
                
                # Substitui as ocorrências de - ./mgc ... por ```./mgc ...``` removendo o '-'
                formatted_content = re.sub(r'- (\./mgc [^\n]*)', r'```\1```', content)
                
                # Remove crases no final do texto
                formatted_content = re.sub(r'```(.*?)```', r'```\n\1\n```', formatted_content)
                
                with open(file_path, 'w') as file:
                    file.write(formatted_content)
                
                print(f"Updated {file_path} with formatted ./mgc commands")


def format_dash_dash_commands(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                
                with open(file_path, 'r') as file:
                    content = file.read()
                
                # Substitui as ocorrências de - --<qualquer_texto> por - `--<qualquer_texto>`
                formatted_content = re.sub(r'- (--[^\s]+)', r'- `\1`', content)
                
                with open(file_path, 'w') as file:
                    file.write(formatted_content)
                
                print(f"Updated {file_path} with formatted --<qualquer_texto> commands")

# Diretório raiz da sua estrutura de pastas
root_directory = 'C:\\Users\\LU_PICOLOTO\\Documents\\portal-cloud\\docs-magalu-cloud\\docs\\cli-mgc\\commands-reference'
update_help_md(root_directory)
move_single_file_folders(root_directory)
insert_sidebar_position(root_directory)
remove_hash_from_line_6(root_directory)
format_mgc_commands(root_directory)
format_dash_dash_commands(root_directory)

