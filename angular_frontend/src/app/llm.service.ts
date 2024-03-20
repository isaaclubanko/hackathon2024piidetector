import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { PIIResponseAdapter, PIIResponseModel } from './models/pii-response.model'
import { Observable, map } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class LlmService {

  constructor(
    private http: HttpClient
  ) { }

  public refreshAPI(){
    return this.http.get<string>('/api/')
  }

  public postText(inputText:string):Observable<PIIResponseModel[]>{
    // return this.http.post<any[]>('/api/detect_pii/', {text_input: inputText})

    return this.http.post<any[]>('/api/detect_pii/', {text_input: inputText}).pipe(
      map(data => data.map(item => new PIIResponseAdapter().adapt(item)))
    );
  }

}
