import { Component, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  @ViewChild('fileInput') fileInput!: ElementRef;
  isLoading = false;

  constructor(private http: HttpClient) { }

  onFileSelected(event: Event): void {
    const fileInput = event.target as HTMLInputElement;
    const file = fileInput?.files ? fileInput.files[0] : null;

    if (file) {
      this.uploadFile(file);
      console.log(file);
        } else {
        console.error("No file selected");
    }
  }

  private uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    this.isLoading = true;
    this.http.post('http://localhost:5000/upload', formData, { responseType: 'blob' }).subscribe(
        (response: Blob) => {
            const blob = new Blob([response], { type: 'zip' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'files.csv';
            a.click();
            window.URL.revokeObjectURL(url);
            this.isLoading = false;
        },
        (error) => {
            this.isLoading = false;
            alert('Failed: ' + error.message);
        }
    );
  }
}
