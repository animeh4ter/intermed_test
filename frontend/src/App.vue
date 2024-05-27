<template>
  <v-app>
    <v-main>
      <div class="container">
        <h1 class="title" style="text-align: center">Записи Таблицы</h1>
        <div class="add-button-container">
          <v-btn color="primary" @click="openModal">Добавить запись</v-btn>
        </div>
        <v-dialog v-model="modalOpen">
          <v-card>
            <v-card-title>Добавить запись</v-card-title>
            <v-card-text>
              <v-form ref="form" @submit.prevent="handleSubmit">
                <v-text-field
                    v-model="formData.patient_fio"
                    style="margin-bottom: 10px"
                    label="ФИО пациента"
                    :rules="[v => !!v]">
                </v-text-field>
                <v-text-field
                    v-model="formData.patient_birthdate"
                    style="margin-bottom: 10px"
                    label="Дата рождения пациента"
                    type="date"
                    :rules="[v => !!v]">
                </v-text-field>
                <v-text-field
                    v-model="formData.study_uid"
                    style="margin-bottom: 10px"
                    label="UUID исследования"
                    :rules="[v => !!v]">
                </v-text-field>
                <v-text-field
                    v-model="formData.study_date"
                    style="margin-bottom: 10px"
                    label="Дата исследования"
                    type="datetime-local"
                    :rules="[v => !!v]">
                </v-text-field>
                <v-select
                    v-model="formData.study_modality"
                    style="margin-bottom: 10px"
                    :items="modalities"
                    label="Модальность"
                    :rules="[v => !!v]">
                </v-select>
                <v-btn
                    type="button"
                    color="error"
                    @click="modalOpen = false; errorMsg=''; formData={
                                                            patient_fio: '',
                                                            patient_birthdate: '',
                                                            study_uid: '',
                                                            study_date: '',
                                                            study_modality: '',
                                                          }"
                    style="margin-right: 10px">Отменить
                </v-btn>
                <v-btn type="submit" color="primary">Добавить</v-btn>
                <v-alert
                    v-if="errorMsg"
                    color="error"
                    style="margin-top: 10px">
                  {{errorMsg}}
                </v-alert>
              </v-form>
            </v-card-text>
          </v-card>
        </v-dialog>
        <div class="data-table-container">
          <DataTable/>
        </div>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import DataTable from './components/DataTable.vue'
import axios from "axios";
import '@mdi/font/css/materialdesignicons.css';

export default {
  name: 'App',

  components: {
    DataTable,
  },

  data() {
    return {
      responseData: null,
      modalOpen: false,
      errorMsg: '',
      formData: {
        patient_fio: '',
        patient_birthdate: '',
        study_uid: '',
        study_date: '',
        study_modality: '',
      },
      modalities: [
        'Ultrasound',
        'Echocardiography',
        'Digital Radiography',
        'Positron emission tomography',
        'X-Ray Angiography',
        'Magnetic Resonance',
        'Angioscopy',
        'Computed Radiography',
        'Computed Tomography',
        'Mammography',
      ],
    };
  },

  methods: {
    openModal() {
      this.modalOpen = true;
    },

    async handleSubmit() {
      if (this.isFormValid()) {
        try {
          await axios.post('https://donkey-cheerful-pup.ngrok-free.app/create_new/', this.formData);
          this.resetForm();
          this.modalOpen = false;
          this.errorMsg = ''
        } catch (error) {
          console.log('error')
          this.errorMsg = error.response.data.error
        }
      }
    },

    isFormValid() {
      return Object.values(this.formData).every(value => !!value);
    },

    resetForm() {
      this.formData = {
        patient_fio: '',
        patient_birthdate: '',
        study_uid: '',
        study_date: '',
        study_modality: '',
      };
    }
  },
}
</script>

<style>
.container {
  max-width: 1600px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
}

.add-button-container {
  text-align: center;
  margin-bottom: 20px;
}

.data-table-container {
  background-color: #f0f0f0;
}
</style>