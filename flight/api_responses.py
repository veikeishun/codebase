import base64
from .models import *
from datetime import date, datetime
import requests
from django.http import JsonResponse

terminal_id = "RABOM030009301"
username = "jbtravel"
password = "Riya@123"

def auth():
    credentials = f"{terminal_id}*{username}:{password}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()
    return base64_credentials

def generatetoken():
    current_day = date.today()
    try:
        token_info = TokenInfo.objects.get()
        if token_info.last_generation_date == current_day:
            return token_info.token
    except TokenInfo.DoesNotExist:
        pass
    base64_string = "UkFCT00wMzAwMDkzMDEqamJ0cmF2ZWw6Uml5YUAxMjM="
    endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/Login"
    headers = {
        "Authorization": f"Basic {base64_string}"
    }
    try:
        response = requests.post(endpoint, headers=headers)
        response_json = response.json() 
        tokenn = response_json["Token"]
        token_info = TokenInfo.objects.get()
        token_info.token = tokenn
        token_info.last_generation_date = current_day
        token_info.save()
        return tokenn

    except requests.exceptions.RequestException as e:
        print(e)
        return JsonResponse({"message": "Error during request"}, status=500)

# api responses
def availabilitycheck(flight_type, DepartureStation, ArrivalStation, FlightDate, FlightDateR, FarecabinOption, adult, children, infant):
    tokenn = generatetoken()
    print(tokenn)
    if tokenn is not None:
        endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/Availability"
        headers = {
            "TOKEN": tokenn
        }
        payload = {
            "TripType": flight_type,
            "AirlineID": "",
            "AgentInfo": {
                "AgentId": "RABOM0300093",
                "TerminalId": "RABOM030009301",
                "UserName": "jbtravel",
                "AppType": "API",
                "Version": "V1.0"
            },
            "AvailInfo": [
                {
                    "DepartureStation": DepartureStation,
                    "ArrivalStation": ArrivalStation,
                    "FlightDate": FlightDate,
                    "FarecabinOption": FarecabinOption,
                    "FareType": "N",
                    "OnlyDirectFlight": False
                }
            ],
            "PassengersInfo": {
                "AdultCount": adult,
                "ChildCount": children,
                "InfantCount": infant
            }
        }
        if flight_type == "R":
            payload["AvailInfo"].append({
                "DepartureStation": ArrivalStation,
                "ArrivalStation": DepartureStation,
                "FlightDate": FlightDateR,
                "FarecabinOption": FarecabinOption,
                "FareType": "N",
                "OnlyDirectFlight": False
            })
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            availabilitycheck_Response = response.json()
            return availabilitycheck_Response
                  
        except requests.exceptions.RequestException as e:
            print(e)
            return JsonResponse({"message": "Error during request"}, status=500)


def Pricing(BaseOrigin, BaseDestination, TripType, AdultCount, children, infant, Trackid, FlightID, FlightNumber, Origin, Destination, DepartureDateTime, ArrivalDateTime, FlightID1, FlightNumber1, Origin1, Destination1, DepartureDateTime1, ArrivalDateTime1, TotalBaseAmt, TotalGrossAmt, Stops):
    tokenn = generatetoken()
    print(tokenn)
    if tokenn is not None:
        endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/Pricing"
        headers = {
            "TOKEN": tokenn
        }
        payload = {
                "AgentInfo": {
                    "AgentId": "RABOM0300093",
                    "TerminalId": "RABOM030009301",
                    "UserName": "jbtravel",
                    "AppType": "API",
                    "Version": "V1.0"
                },
                "SegmentInfo": {
                    "BaseOrigin": BaseOrigin,
                    "BaseDestination": BaseDestination,
                
                    "TripType": TripType,
                    "AdultCount": AdultCount,
                    "ChildCount": children,
                    "InfantCount": infant
                },
                "Trackid": Trackid,
                "ItineraryInfo": [
                    {
                        "FlightDetails": [
                            {
                                "FlightID": FlightID,
                                "FlightNumber": FlightNumber,
                                "Origin": Origin,
                                "Destination": Destination,
                                "DepartureDateTime": DepartureDateTime,
                                "ArrivalDateTime": ArrivalDateTime
                            }
                        ],
                        "BaseAmount": TotalBaseAmt,
                        "GrossAmount": TotalGrossAmt
                    }
                ]
            }
        
        if Stops == "1":
            payload["ItineraryInfo"][0]["FlightDetails"].append(
                {
                    "FlightID": FlightID1,
                    "FlightNumber": FlightNumber1,
                    "Origin": Origin1,
                    "Destination": Destination1,
                    "DepartureDateTime": DepartureDateTime1,
                    "ArrivalDateTime": ArrivalDateTime1
                }
            )
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response_pricing = response.json()
            return response_pricing
                  
        except requests.exceptions.RequestException as e:
            print(e)
            return JsonResponse({"message": "Error during request"}, status=500)


def Fare_Rules(FlightID, FlightID1, Trackid, Stops):
    tokenn = generatetoken()
    if tokenn is not None:
        endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/GetFareRule"
    headers = {
            "TOKEN": tokenn
        }
    payload = {
        "AgentInfo": {
                    "AgentId": "RABOM0300093",
                    "TerminalId": "RABOM030009301",
                    "UserName": "jbtravel",
                    "AppType": "API",
                    "Version": "V1.0"
                },
        "FlightsInfo": [
            {
            "FlightID": FlightID
            }
        ],  
        "Trackid": Trackid
        }
    if Stops == "1":
        payload["FlightsInfo"].append(
            {
            "FlightID": FlightID1
            }
            )
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response_fare_rules = response.json()
        return response_fare_rules        
    except requests.exceptions.RequestException as e:
        print(e)
        return JsonResponse({"message": "Error during request"}, status=500)

def Booking(AdultCount, ChildCount, InfantCount, Token, FlightID, FlightNumber, Origin, Destination, DepartureDateTime, ArrivalDateTime, TotalAmount, PaxDetailsInfo, TripType, TrackId, Stops, FlightID1, FlightNumber1, Origin1, Destination1, DepartureDateTime1, ArrivalDateTime1):
    tokenn = generatetoken()
    print(tokenn)
    if tokenn is not None:
        endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/Book"
        headers = {
            "TOKEN": tokenn
        }
        payload = {
                    "AgentInfo": {
                    "AgentId": "RABOM0300093",
                    "TerminalId": "RABOM030009301",
                    "UserName": "jbtravel",
                    "AppType": "API",
                    "Version": "V1.0"
                    },
                    "AdultCount": int(AdultCount),
                    "ChildCount": int(ChildCount),
                    "InfantCount": int(InfantCount),
                    "ItineraryFlightsInfo": [
                        {
                            "Token": Token,
                            "FlighstInfo": [
                                {
                                    "FlightID": FlightID,
                                    "FlightNumber": FlightNumber,
                                    "Origin": Origin,
                                    "Destination": Destination,
                                    "DepartureDateTime": DepartureDateTime,
                                    "ArrivalDateTime": ArrivalDateTime
                                }
                            ],
                            "PaymentMode": "T",
                            "SeatsSSRInfo": [],
                            "BaggSSRInfo": [],
                            "MealsSSRInfo": [],
                            "OtherSSRInfo": [],
                            "PaymentInfo": [
                                {
                                    "TotalAmount": TotalAmount
                                }
                            ]
                        }
                    ],
                    "PaxDetailsInfo": PaxDetailsInfo,
                    "AddressDetails": {
                        "CountryCode": "91",
                        "ContactNumber": "9840688337",
                        "EmailID": "udayd2k@gmail.com"
                    },
                    "GSTInfo": {
                        "GSTNumber": "",
                        "GSTCompanyName": "",
                        "GSTAddress": "",
                        "GSTEmailID": "",
                        "GSTMobileNumber": ""
                    },
                    "TripType": TripType,
                    "BlockPNR": False,
                    "BaseOrigin": Origin,
                    "BaseDestination": "",
                    "TrackId": TrackId
                }
        if Stops == "1":
            payload['BaseDestination'] = Destination1
        else:
            payload['BaseDestination'] = Destination


        if Stops == "1":
            payload["ItineraryFlightsInfo"][0]["FlighstInfo"].append(
                    {
                        "FlightID": FlightID1,
                        "FlightNumber": FlightNumber1,
                        "Origin": Origin1,
                        "Destination": Destination1,
                        "DepartureDateTime": DepartureDateTime1,
                        "ArrivalDateTime": ArrivalDateTime1
                    }
            )
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response_booking = response.json()
            return response_booking
                  
        except requests.exceptions.RequestException as e:
            print(e)
            return JsonResponse({"message": "Error during request"}, status=500)


#round trip
def Rpricing(BaseOrigin, BaseDestination, TripType, AdultCount, children, infant, Trackid, FlightID, FlightNumber, Origin, Destination, DepartureDateTime, ArrivalDateTime, FlightID1, FlightNumber1, Origin1, Destination1, DepartureDateTime1, ArrivalDateTime1, TotalBaseAmt, OneWay_TotalGrossAmt, Stops, RFlightID, RFlightNumber, ROrigin, RDestination, RDepartureDateTime, RArrivalDateTime, RFlightID1, RFlightNumber1, ROrigin1, RDestination1, RDepartureDateTime1, RArrivalDateTime1, RTotalBaseAmt, ROneWay_TotalGrossAmt, RStops):
    tokenn = generatetoken()
    print(tokenn)
    if tokenn is not None:
        endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/Pricing"
        headers = {
            "TOKEN": tokenn
        }
        payload = {
                "AgentInfo": {
                    "AgentId": "RABOM0300093",
                    "TerminalId": "RABOM030009301",
                    "UserName": "jbtravel",
                    "AppType": "API",
                    "Version": "V1.0"
                },
            "SegmentInfo": {
                "BaseOrigin": BaseOrigin,
                "BaseDestination": "",
            
                "TripType": TripType,
                "AdultCount": AdultCount,
                "ChildCount": children,
                "InfantCount": infant
            },
            "Trackid": Trackid,
            "ItineraryInfo": [
                {
                    "FlightDetails": [
                        {
                            "FlightID": FlightID,
                            "FlightNumber": FlightNumber,
                            "Origin": Origin,
                            "Destination": Destination,
                            "DepartureDateTime": DepartureDateTime,
                            "ArrivalDateTime": ArrivalDateTime
                        }
                    ],
                    "BaseAmount": TotalBaseAmt,
                    "GrossAmount": OneWay_TotalGrossAmt
                },
                {
                    "FlightDetails": [
                        {
                            "FlightID": RFlightID,
                            "FlightNumber": RFlightNumber,
                            "Origin": ROrigin,
                            "Destination": RDestination,
                            "DepartureDateTime": RDepartureDateTime,
                            "ArrivalDateTime": RArrivalDateTime
                        }
                    ],
                    "BaseAmount": RTotalBaseAmt,
                    "GrossAmount": ROneWay_TotalGrossAmt
                }
            ]
        }

        if Stops == "1":
            payload['SegmentInfo']['BaseDestination'] = Destination1
        else:
            payload['SegmentInfo']['BaseDestination'] = Destination


        if Stops == "1":
            payload["ItineraryInfo"][0]["FlightDetails"].append(
                {
                    "FlightID": FlightID1,
                    "FlightNumber": FlightNumber1,
                    "Origin": Origin1,
                    "Destination": Destination1,
                    "DepartureDateTime": DepartureDateTime1,
                    "ArrivalDateTime": ArrivalDateTime1
                }
            )

        if RStops == "1":
            payload["ItineraryInfo"][1]["FlightDetails"].append(
                {
                    "FlightID": RFlightID1,
                    "FlightNumber": RFlightNumber1,
                    "Origin": ROrigin1,
                    "Destination": RDestination1,
                    "DepartureDateTime": RDepartureDateTime1,
                    "ArrivalDateTime": RArrivalDateTime1
                }
            )

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        Rresponse_pricing = response.json()
        return Rresponse_pricing
                  
    except requests.exceptions.RequestException as e:
        print(e)
        return JsonResponse({"message": "Error during request"}, status=500)
    
def RBooking(AdultCount, ChildCount, InfantCount, Token, FlightID, FlightNumber, Origin, Destination, DepartureDateTime, ArrivalDateTime, TotalAmount, RToken, RFlightID, RFlightNumber, ROrigin, RDestination, RDepartureDateTime, RArrivalDateTime, RTotalAmount, PaxDetailsInfo, TripType, TrackId, Stops, RStops, FlightID1, FlightNumber1, Origin1, Destination1, DepartureDateTime1, ArrivalDateTime1, RFlightID1, RFlightNumber1, ROrigin1, RDestination1, RDepartureDateTime1, RArrivalDateTime1):
    tokenn = generatetoken()
    print(tokenn)
    if tokenn is not None:
        endpoint = "http://testrws.mywebcheck.in/TravelAPI.svc/Book"
        headers = {
            "TOKEN": tokenn
        }
        payload = {
                 "AgentInfo": {
                        "AgentId": "RABOM0300093",
                        "TerminalId": "RABOM030009301",
                        "UserName": "jbtravel",
                        "AppType": "API",
                        "Version": "V1.0"
                    },
                    "AdultCount": AdultCount,
                    "ChildCount": ChildCount,
                    "InfantCount": InfantCount,
                    "ItineraryFlightsInfo": [
                        {           
                            "Token": Token,
                            "FlighstInfo": [
                                {
                                    "FlightID": FlightID,
                                    "FlightNumber": FlightNumber,
                                    "Origin": Origin,
                                    "Destination": Destination,
                                    "DepartureDateTime": DepartureDateTime,
                                    "ArrivalDateTime": ArrivalDateTime
                                }
                            ],
                            "PaymentMode": "T",           
                            "SeatsSSRInfo": [],
                            "BaggSSRInfo": [],
                            "MealsSSRInfo": [],
                            "OtherSSRInfo": [],
                            "PaymentInfo": [
                                {
                                    "TotalAmount": TotalAmount                                    
                                }
                            ]
                        },
                        {           
                            "Token": RToken,
                            "FlighstInfo": [
                                {
                                    "FlightID": RFlightID,
                                    "FlightNumber": RFlightNumber,
                                    "Origin": ROrigin,
                                    "Destination": RDestination,
                                    "DepartureDateTime": RDepartureDateTime,
                                    "ArrivalDateTime": RArrivalDateTime
                                }
                            ],
                            "PaymentMode": "T",           
                            "SeatsSSRInfo": [],
                            "BaggSSRInfo": [],
                            "MealsSSRInfo": [],
                            "OtherSSRInfo": [],
                            "PaymentInfo": [
                                {
                                    "TotalAmount": RTotalAmount                                    
                                }
                            ]
                        }
                    ],
                    "PaxDetailsInfo": PaxDetailsInfo,
                    "AddressDetails": {
                        "CountryCode": "91",
                        "ContactNumber": "9886325377",
                        "EmailID": "test123@gmail.com"
                    },
                    "GSTInfo": {
                        "GSTNumber": "",
                        "GSTCompanyName": "",
                        "GSTAddress": "",
                        "GSTEmailID": "",
                        "GSTMobileNumber": ""
                    
                    },
                    "TripType": TripType,   
                    "BlockPNR": False,
                    "BaseOrigin": Origin,
                    "BaseDestination": "",
                    "TrackId": TrackId
                }


        if Stops == "1":
            payload['BaseDestination'] = Destination1
        else:
            payload['BaseDestination'] = Destination


        if Stops == "1":
            payload["ItineraryFlightsInfo"][0]["FlighstInfo"].append(
                    {
                        "FlightID": FlightID1,
                        "FlightNumber": FlightNumber1,
                        "Origin": Origin1,
                        "Destination": Destination1,
                        "DepartureDateTime": DepartureDateTime1,
                        "ArrivalDateTime": ArrivalDateTime1
                    }
            )

        if RStops == "1":
            payload["ItineraryFlightsInfo"][1]["FlighstInfo"].append(
                    {
                        "FlightID": RFlightID1,
                        "FlightNumber": RFlightNumber1,
                        "Origin": ROrigin1,
                        "Destination": RDestination1,
                        "DepartureDateTime": RDepartureDateTime1,
                        "ArrivalDateTime": RArrivalDateTime1
                    }
            )
        try:
            print(payload)
            response = requests.post(endpoint, headers=headers, json=payload)
            Rresponse_booking = response.json()
            return Rresponse_booking
                  
        except requests.exceptions.RequestException as e:
            print(e)
            return JsonResponse({"message": "Error during request"}, status=500)

