#include <string>
#include <filesystem>

int check_for_file_path(std::string path_location) {
    std::filesystem::path file_path(path_location);

    if (std::filesystem::exists(file_path) == true) {
        return 1;
    } else {
        return 0;
    }
}