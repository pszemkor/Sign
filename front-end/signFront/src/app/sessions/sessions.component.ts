import { Component, OnInit } from '@angular/core';
import { SessionsService } from '../services/sessions.service';
import { Session } from '../shared/session';
@Component({
  selector: 'app-sessions',
  templateUrl: './sessions.component.html',
  styleUrls: ['./sessions.component.scss']
})
export class SessionsComponent implements OnInit {
  sessions: Session[];
  constructor(private sessionService: SessionsService) { }

  ngOnInit(): void {
    this.sessionService.getSessions()
      .subscribe(data => this.sessions = data)
  }



}
