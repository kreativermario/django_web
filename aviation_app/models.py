from django.db import models


class Airline(models.Model):
    airline_name = models.CharField(max_length=50)  # Airline name
    country = models.CharField(max_length=50)  # Country of the airline
    creation_date = models.DateField()  # Creation date of the airline

    def __str__(self):
        return self.airline_name


class Aircraft(models.Model):
    registration = models.CharField(max_length=10)  # CS-TVA
    aircraft_model = models.CharField(max_length=50)  # B737-800NG
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        return self.registration


class Airport(models.Model):
    icao_code = models.CharField(max_length=4)  # ICAO code
    iata_code = models.CharField(max_length=3)  # IATA code
    name = models.CharField(max_length=100)  # Airport name
    country_code = models.CharField(max_length=3)  # Country Code
    location = models.CharField(max_length=50)  # Coordinates
    municipality = models.CharField(max_length=50)  # Municipality e.g (Vienna)

    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)  # Flight number
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)  # Airline
    check_in_desk = models.CharField(max_length=10)  # Check-in desks
    gate = models.CharField(max_length=10)  # Gate number
    terminal = models.CharField(max_length=10)  # Airport terminal

    local_departure_time = models.DateTimeField()
    local_arrival_time = models.DateTimeField()
    actual_departure_time = models.DateTimeField()
    actual_arrival_time = models.DateTimeField()

    flight_status = models.CharField(max_length=35)

    distance_in_kms = models.DecimalField(max_digits=10, decimal_places=2)
    distance_in_nms = models.DecimalField(max_digits=10, decimal_places=2)
    distance_in_miles = models.DecimalField(max_digits=10, decimal_places=2)

    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE,
                                          related_name='departing_flights')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE,
                                        related_name='arriving_flights')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    def __str__(self):
        return self.flight_number



