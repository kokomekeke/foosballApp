<template>
  <div class="bg-blue-500 grid grid-cols-5 grid-rows-3 gap-4 h-screen items-center justify-items-center">
    <div class="bg-gray-200 row-span-2 w-full h-full col-span-2">
      <MapComponent :isLocationSet="isLocationSet" :location="location"></MapComponent>
    </div>
    <div>2</div>
    <div>3</div>
    <div class="row-span-2 bg-gray-400 w-full h-full grid grid-row-6 grid-col-3">
      <div class="w-full h-full">
        <label for="minmax-range" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          Posterize
        </label>
        <input
          v-model="range"
          id="minmax-range"
          type="range"
          min="0"
          max="100"
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
          :disabled="isDisabled"
        />
      </div>
    </div>
    <div class="bg-pink-300 w-full h-full grid grid-rows-1 place-items-center">
      <button
        class="w-24 rounded-sm border-2 border-solid bg-pink-500 active:bg-pink-700 transition"
        @click="triggerFileInput"
      >
        Insert Image
      </button>
      <input
        type="file"
        ref="fileInput"
        @change="handleFileUpload"
        accept="image/*"
        class="hidden"
      />
    </div>
    <div>7</div>
    <div class="w-full h-full col-span-2 bg-blue-300">
      <button v-if="imageUrl" @click="upload">Upload Image</button>
    </div>
    <div class="w-full h-full col-span-3 bg-blue-700 flex justify-center items-center">
      <img v-if="imageUrl" :src="imageUrl" alt="Selected Image" class="mt-2 mb-2 h-full" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import MapComponent from "./components/MapComponent.vue";

const imageUrl = ref(null);
const fileInput = ref(null);
const isDisabled = ref(true);
const range = ref(5);
const isLocationSet = ref(false)
const location = ref([40, 40])


// Fájlválasztó megnyitása
const triggerFileInput = () => {
  fileInput.value.click();
};


const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    isDisabled.value = false;
    imageUrl.value = URL.createObjectURL(file); // Eredeti kép előnézete
  }
};


const upload = async () => {
  const file = fileInput.value.files[0];
  if (!file) {
    console.error("Nincs fájl kiválasztva!");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  try {
    const res = await axios.post("http://localhost:5000/api/edit-image", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    console.log("Siker:", res.data);
  } catch (error) {
    console.error("Hiba:", error);
  }

  try {
    const res = await axios.get("http://localhost:5000/api/geoloc");

    if (res.data.warning) {
        console.warn("Nincs EXIF adat:", res.data.warning);
    } else {
      console.log("EXIF adatok:", res.data.exif_data);
      location.value = res.data.exif_data
      console.log(location.value)
      isLocationSet.value = true
    }
} catch (error) {
    console.error("Hiba:", error.response ? error.response.data : error.message);
}
};

// Figyeli a slider változását és elküldi a szerverre az új értéket
watch(range, () => {
  posterize();
});

// Posterizált kép lekérése szerverről
const posterize = async () => {
  const file = fileInput.value.files[0];
  if (!file) {
    console.error("Nincs fájl kiválasztva!");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);
  formData.append("posterize_level", range.value); // Küldjük a slider értékét

  try {
    const res = await axios.post("http://localhost:5000/api/posterize", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      responseType: "blob", // Visszakapott kép bináris formátumban
    });

    // Blob formátumú válaszból URL létrehozása és megjelenítés
    const imageBlob = new Blob([res.data], { type: "image/png" });
    imageUrl.value = URL.createObjectURL(imageBlob);

    console.log("Posterized kép frissítve!");
  } catch (error) {
    console.error("Hiba:", error);
  }


};
</script>

<style scoped>

</style>
