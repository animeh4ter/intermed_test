<template>
  <v-app>
    <v-container>
      <v-text-field v-model="globalSearch" label="Фильтр по всем столбцам"></v-text-field>
      <div class="search-section">
        <div class="search-fields">
            <v-text-field v-model="search" label="ФИО"></v-text-field>
            <v-text-field v-model="birthdateSearch" label="Дата рождения"></v-text-field>
            <v-text-field v-model="studyUidSearch" label="UUID исследования"></v-text-field>
            <v-text-field v-model="studyDateSearch" label="Дата исследования"></v-text-field>
            <v-autocomplete
              v-model="modalitySearch"
              :items="modalities"
              label="Модальность"
              dense
              :headers="headers"
              class="fixed-width-autocomplete"
            ></v-autocomplete>
        </div>
      </div>
      <v-row>
        <br>
      </v-row>
      <v-data-table
          :items="filteredItems"
          multi-sort
          :loading="loading"
          @update:page="handlePagination"
          :items-per-page-options="[{value: 10, title: '10'},
                                    {value: 25, title: '25'},
                                    {value: 50, title: '50'},
                                    ]"
        >

      </v-data-table>
    </v-container>
  </v-app>
</template>

<script setup>
import { ref, onMounted, computed, watch} from 'vue';
import axios from 'axios';

const items = ref([]);
const search = ref('');
const birthdateSearch = ref('');
const studyUidSearch = ref('');
const studyDateSearch = ref('');
const modalitySearch = ref(null);
const globalSearch = ref('');
const page = ref(1);
const hasNext = ref(true);
const loading = ref(false);

const headers = [
  { text: 'ФИО пациента', value: 'ФИО пациента' },
  { text: 'Дата рождения пациента', value: 'Дата рождения пациента' },
  { text: 'UUID исследования', value: 'UUID исследования' },
  { text: 'Дата исследования', value: 'Дата исследования' },
  { text: 'Модальность', value: 'Модальность' },
];


const filteredItems = computed(() => {
  let result = items.value;

  if (globalSearch.value) {
    const searchStr = globalSearch.value.toLowerCase();
    result = result.filter(item =>
      Object.values(item).some(val =>
        String(val).toLowerCase().includes(searchStr)
      )
    );
  }

  return result;
});

const loadMore = async () => {
  if (loading.value || !hasNext.value) return;
  loading.value = true;
  try {
    const response = await axios.get('https://donkey-cheerful-pup.ngrok-free.app/get_db_data/', {
      params: {
        page: page.value,
        search: search.value,
        birthdateSearch: birthdateSearch.value,
        studyUidSearch: studyUidSearch.value,
        studyDateSearch: studyDateSearch.value,
        modalitySearch: modalitySearch.value,
        globalSearch: globalSearch.value,
      }
    });
    items.value.push(...response.data.data);
    hasNext.value = response.data.has_next;
    page.value += 1;
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
  } finally {
    loading.value = false;
  }
};

const modalities = [
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
];

const handlePagination = () => {
  loadMore();
};

watch([search, birthdateSearch, studyUidSearch, studyDateSearch, modalitySearch, globalSearch], () => {
  items.value = [];
  page.value = 1;
  hasNext.value = true;
  loadMore();
});

onMounted(() => {
  loadMore();
  const footerInfo = document.querySelector('.v-data-table-footer__info');
  if (footerInfo) {
    footerInfo.style.display = 'none';
  }
  const footerLast = document.querySelector('.v-pagination__last');
  if (footerLast) {
    footerLast.style.display = 'none';
  }
  const footerFirst = document.querySelector('.v-pagination__first');
  if (footerFirst) {
    footerFirst.style.display = 'none';
  }
});
</script>

<style>
.search-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-fields {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex: 1;
}

.fixed-width-autocomplete {
  max-width: 200px;
}

.search-fields > *:first-child {
  width: 1%;
}
</style>
