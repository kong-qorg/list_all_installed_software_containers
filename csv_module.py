import csv


def convert_to_csv(data):

    with open('output.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Container Id', 'Container Name', 'Software Lists']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            row['Software Lists'] = ','.join([f'{k}={v}' for k, v in row['Software Lists']])
            writer.writerow(row)
