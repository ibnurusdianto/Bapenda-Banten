// Fungsi untuk menampilkan pertanyaan berikutnya
function nextQuestion(nextQuestionId, event) {
  event.preventDefault(); // Mencegah pemrosesan bawaan dari tautan
  document.getElementById('question1').style.display = 'none'; // Sembunyikan pertanyaan saat ini
  document.getElementById(nextQuestionId).style.display = 'block'; // Tampilkan pertanyaan berikutnya
}

// Fungsi untuk menampilkan pertanyaan sebelumnya
function previousQuestion(previousQuestionId, event) {
  event.preventDefault(); // Mencegah pemrosesan bawaan dari tautan
  document.getElementById('question2').style.display = 'none'; // Sembunyikan pertanyaan saat ini
  document.getElementById(previousQuestionId).style.display = 'block'; // Tampilkan pertanyaan sebelumnya
}