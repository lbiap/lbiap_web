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
    this.http.post('http://localhost:5000/upload', formData, { responseType: 'text' }).subscribe(
      (response: string) => {
          // response is now correctly treated as a string
          const url = response; // URL from the response
          const a = document.createElement('a');
          a.href = url;
          a.download = 'files.zip'; // Set the default file name for the download
          document.body.appendChild(a); // Append the element to the body
          a.click();
          console.log(url);
          document.body.removeChild(a); // Clean up the DOM by removing the 'a' element
          this.isLoading = false;
      },
      (error) => {
          this.isLoading = false;
          console.error('Upload error:', error);
          alert('Upload failed. See console for details.');
      }
  );
  }
}
