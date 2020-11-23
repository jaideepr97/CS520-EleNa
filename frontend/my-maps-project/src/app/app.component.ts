import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MinLengthValidator } from '@angular/forms';

@Component({
    selector: 'app-root',
    template:'<agm-marker [latitude]="route[0][0]" [longitude]="route[1][1]" *ngFor="let route of {{routes}}; let i=index"></agm-marker>',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent { 
  constructor(private http: HttpClient) { }

  title="EleNa - Elevation based Navigation";
  
  serverUrl = 'http://localhost:8000/find_route/'
  
  coordinates = {
    originLat: 42.3504489,
    originLng: -72.5274984,
    destinationLat: 42.3777404,
    destinationLng: -72.5198350
  }

  locations = []

  elevation_choice: String = "min";
  percentage_of_shortest_distance = 0;
  
  origin = { lat: 42.350489, lng: -72.527421 };
  destination = { lat: 42.451643, lng: -72.565172 };

  setOriginCoordinates($event: any) {
    console.log($event);
    this.coordinates["originLat"] = $event.latLng.lat();;
    this.coordinates["originLng"] = $event.latLng.lng();;
  }

  setDestinationCoordinates($event: any) {
    console.log($event);
    this.coordinates["destinationLat"] = $event.latLng.lat();;
    this.coordinates["destinationLng"] = $event.latLng.lng();;
  }

  onGetDirectionClick(){
    document.getElementById("MyDiv").innerHTML = "";
    const headers = { 'content-type': 'application/json'}  
    let data = {"source_latitude": this.coordinates["originLat"], 
    "source_longitude": this.coordinates["originLng"], 
    "destination_latitude": this.coordinates["destinationLat"], 
    "destination_longitude": this.coordinates["destinationLng"], 
    "percentage": this.percentage_of_shortest_distance, 
    "elevation_type": this.elevation_choice, 
    "algorithm": "a_star"}
    const body=JSON.stringify(data);
    console.log(body)
    this.http.post(this.serverUrl, body,{'headers':headers}).toPromise()
    .then(
      res => { 
        console.log(res);
        this.setRoute(res);
      }
    );
  }

  setRoute(response){
    let routes = response['route']
    console.log(routes)
    this.locations = []
    for (let entry of routes) {
      let new_coordinate = {}
      this.locations.push({"lat": entry[0], "lng": entry[1]});
    }
    console.log(this.locations);
    document.getElementById("MyDiv").innerHTML = "<p>Total Elevation : " + response["elevation"] + 
    "<br /> Total Distance : "+ response["distance"] + "</p>"
  }
}