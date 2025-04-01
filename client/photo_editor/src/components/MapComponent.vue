<template>
  <form>
    <label for="zoom">Zoom:</label>
    <input type="number" id="zoom" v-model="zoom" />
  </form>

  <ol-map style="height: 400px">
    <ol-view
      ref="view"
      :center="center"
      :rotation="rotation"
      :zoom="zoom"
      :projection="projection"
      @change:center="centerChanged"
      @change:resolution="resolutionChanged"
      @change:rotation="rotationChanged"
    />

    <ol-tile-layer>
      <ol-source-osm />
    </ol-tile-layer>
    <ol-vector-layer v-if="props.isLocationSet">
      <ol-source-vector>
        <ol-feature>
          <ol-geom-point :coordinates="[props.location[1], props.location[0]]"></ol-geom-point>
          <ol-style>
            <ol-style-circle :radius="radius">
              <ol-style-fill :color="fill"></ol-style-fill>
              <ol-style-stroke
                :color="stroke"
                :width="strokeWidth"
              ></ol-style-stroke>
            </ol-style-circle>
          </ol-style>
        </ol-feature>
      </ol-source-vector>
    </ol-vector-layer>
<!--    <ol-rotate-control></ol-rotate-control>-->
<!--    <ol-interaction-link />-->
  </ol-map>

  <ul>
    <li>center : {{ currentCenter }}</li>
    <li>resolution : {{ currentResolution }}</li>
    <li>zoom : {{ currentZoom }}</li>
    <li>rotation : {{ currentRotation }}</li>
  </ul>
</template>

<script setup lang="ts">
import {ref, watch} from "vue";

const center = ref([40, 40]);
const projection = ref("EPSG:4326");
const zoom = ref(8);
const rotation = ref(0);
const radius = ref(4);
const currentCenter = ref(center.value);
const currentZoom = ref(zoom.value);
const currentRotation = ref(rotation.value);
const currentResolution = ref(0);
const strokeWidth = ref(10);
const stroke = ref("#ff0000");
const fill = ref("#ffffff");
// const coordinate = defineModel({ default: [40, 40] })

const props = defineProps<{
  isLocationSet: boolean;
  location: number[];
}>();


function resolutionChanged(event) {
  currentResolution.value = event.target.getResolution();
  currentZoom.value = event.target.getZoom();
}
function centerChanged(event) {
  currentCenter.value = event.target.getCenter();
}
function rotationChanged(event) {
  currentRotation.value = event.target.getRotation();
}

watch(
  () => [props.location, props.isLocationSet],
  ([newLocation, newIsLocationSet], [oldLocation, oldIsLocationSet]) => {
    if (newLocation) {
      console.log("📍 Új helyzet (eredeti):", newLocation);
      console.log("📍 Új helyzet (OL formátum):", [newLocation[1], newLocation[0]]);
    }
  },
  { deep: true }
);
</script>

<style scoped>

</style>