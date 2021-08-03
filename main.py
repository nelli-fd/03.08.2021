# Function to find the brightest N stars. It gets as parameters the file (1st),
# coordinates of the given point (2nd and 3rd), the size of the field of view (4th and 5th),
# and how many stars should be in the final file (6th)
def find_N_brightest_stars(f, ra_coordinate, dec_coordinate,
                           fov_horizontal_length, fov_vertical_length,
                           number_of_brightest_stars):
    # Open the file and read only 2nd line. Get a list of columns names
    with open(f, 'r') as fr:
        first_line = fr.readlines()[1: 2]
        first_line = first_line[0].split()

    with open(f, 'r') as fr:
        # Find field of view boundaries
        left_boundary_h = ra_coordinate - fov_horizontal_length / 2
        right_boundary_h = ra_coordinate + fov_horizontal_length / 2
        bottom_boundary_v = dec_coordinate - fov_vertical_length / 2
        top_boundary_v = dec_coordinate + fov_vertical_length / 2

        temp_dict = {}  # Temporary dict for keeping column name and corresponding value of each line
        list_of_stars_in_the_fov = []  # List to hold necessary data to be written in resulted file
        # Start reading the file from the 3rd line line by line where values are represented
        for line in fr.readlines()[2:]:
            line = [line.split('\t') for _ in line.splitlines()][0]  # Split line by tabs
            for i in range(len(first_line)):
                temp_dict[first_line[i]] = line[i]  # Add values to temp_dict
            # Check whether the star is in the field of view
            if left_boundary_h < float(temp_dict['ra_ep2000']) < right_boundary_h \
                    and bottom_boundary_v < float(temp_dict['dec_ep2000']) < top_boundary_v:
                # Calculate the star's distance from the center of the field of view (given point)
                distance = ((float(temp_dict['ra_ep2000']) - ra_coordinate) ** 2
                            + (float(temp_dict['dec_ep2000']) - dec_coordinate) ** 2) ** 0.5
                # Add those stars list to the list_of_stars_in_the_fov
                list_of_stars_in_the_fov.append(list([float(temp_dict['source_id']),
                                                      float(temp_dict['ra_ep2000']),
                                                      float(temp_dict['dec_ep2000']),
                                                      float(temp_dict['phot_g_mean_mag']),
                                                      distance]))
        merge_sort(list_of_stars_in_the_fov, 3)  # Sort the list by magnitude of stars
        if number_of_brightest_stars <= len(list_of_stars_in_the_fov):
            list_of_stars_in_the_fov = list_of_stars_in_the_fov[: number_of_brightest_stars]
        else:
            print('There are only', len(list_of_stars_in_the_fov), 'stars in this field of view!')
        merge_sort(list_of_stars_in_the_fov, 4)  # Sort the list by distance of stars

    # Open the file for writing the data of stars contained in the field of view
    with open('first_task.csv', 'a') as fw:
        fw.write('source_id\t' + 'ra_ep2000\t' + 'dec_ep2000\t' + 'phot_g_mean_mag\t' + 'distance\n')
        for i in range(len(list_of_stars_in_the_fov)):
            for j in range(len(list_of_stars_in_the_fov[i])):
                if j < len(list_of_stars_in_the_fov[i]) - 1:
                    fw.write(str(list_of_stars_in_the_fov[i][j]) + '\t')
                else:
                    fw.write(str(list_of_stars_in_the_fov[i][j]) + '\n')


# Function for sorting.
# First parameter is the list of stars, second parameter shows the index of the element by which it should be sorted
def merge_sort(list_of_stars_inside_the_fov, index):
    if len(list_of_stars_inside_the_fov) > 1:
        # Find the middle point of the list and divide it into two halves
        mid = len(list_of_stars_inside_the_fov) // 2
        left_half = list_of_stars_inside_the_fov[:mid]
        right_half = list_of_stars_inside_the_fov[mid:]

        # Call the function recursively for the first half and second half
        merge_sort(left_half, index)
        merge_sort(right_half, index)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][index] < right_half[j][index]:
                list_of_stars_inside_the_fov[k] = left_half[i]
                i += 1
            else:
                list_of_stars_inside_the_fov[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            list_of_stars_inside_the_fov[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            list_of_stars_inside_the_fov[k] = right_half[j]
            j += 1
            k += 1


# Driver code
if __name__ == '__main__':
    file = 'cleaned_stars.tsv'
    ra = int(input('Input ra: '))
    dec = int(input('Input dec: '))
    fov_h = int(input('Input horizontal field of view: '))
    fov_v = int(input('Input vertical field of view: '))
    number_of_stars = int(input('Input number of stars: '))
    find_N_brightest_stars(file, ra, dec, fov_h, fov_v, number_of_stars)
    print()
