import { Component, OnInit } from '@angular/core';
import { LetterService } from '../services/letter.service'
import { interval } from 'rxjs';
import { Result } from '../shared/result';
@Component({
  selector: 'app-trainer',
  templateUrl: './trainer.component.html',
  styleUrls: ['./trainer.component.scss']
})
export class TrainerComponent implements OnInit {
  currentLetter: string = "X";
  result: Result;
  printSuccess: boolean;
  constructor(private letterService: LetterService) {
  }

  ngOnInit(): void {
    this.letterService.getLetterToRecognize()
      .subscribe(current => this.currentLetter = current["letter"])
      interval(200)
      .subscribe(x => this.letterService.checkIfSuccess()
        .subscribe(res => {
          this.result = res;
          if (res.success) {
            this.currentLetter = res.new_letter;
            this.printSuccess = true;
            console.log("new letter: " + this.currentLetter)
          }else{
            this.printSuccess = false
          }
        }))
  }

  // onStart() {
  //   this.letterService.getLetterToRecognize()
  //     .subscribe(current => { console.log(current["letter"]); this.currentLetter = current["letter"] });
  // }

  onSkip() {
    this.letterService.skipLetter()
    .subscribe(res => this.currentLetter = res.new_letter)
  }


}