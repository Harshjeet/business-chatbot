<template>
  <div class="container">
    <h1>AI Business Insights Assistant</h1>
    
    <div class="query-section">
      <div class="form-group">
        <label>Analysis Type:</label>
        <select v-model="analysisType" class="form-control">
          <option value="competitive_analysis">Competitive Analysis</option>
          <option value="trend_forecasting">Trend Forecasting</option>
        </select>
      </div>

      <div class="form-group" v-if="analysisType === 'competitive_analysis'">
        <label>Company Name:</label>
        <input v-model="params.company" type="text" class="form-control">
      </div>

      <div class="form-group">
        <label>Industry:</label>
        <input v-model="params.industry" type="text" class="form-control">
      </div>

      <div class="form-group" v-if="analysisType === 'trend_forecasting'">
        <label>Timeframe:</label>
        <input v-model="params.timeframe" type="text" class="form-control">
      </div>

      <button @click="analyze" class="btn-primary">Generate Insights</button>
    </div>

    <div v-if="loading" class="loading">Analyzing...</div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="results" class="results-section">
      <h2>Analysis Results</h2>
      
      <div class="overview-section">
        <h3>Overview</h3>
        <p>{{ results.overview }}</p>
      </div>

      <div class="competitors-section" v-if="analysisType === 'competitive_analysis'">
        <h3>Competitor Analysis</h3>
        <div v-for="(competitor, index) in results.competitors" :key="index" class="competitor-card">
          <h4>{{ competitor.name }} ({{ competitor.market_share }})</h4>
          <div class="strengths">
            <h5>Strengths</h5>
            <ul>
              <li v-for="(strength, sIndex) in competitor.strengths" :key="sIndex">{{ strength }}</li>
            </ul>
          </div>
          <div class="weaknesses">
            <h5>Weaknesses</h5>
            <ul>
              <li v-for="(weakness, wIndex) in competitor.weaknesses" :key="wIndex">{{ weakness }}</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="recommendations-section" v-if="results.recommendation">
        <h3>Strategic Recommendations</h3>
        <div class="recommendation-type">
          <h4>Short Term</h4>
          <ul>
            <li v-for="(rec, index) in results.recommendation.short_term" :key="'short-'+index">{{ rec }}</li>
          </ul>
        </div>
        <div class="recommendation-type">
          <h4>Long Term</h4>
          <ul>
            <li v-for="(rec, index) in results.recommendation.long_term" :key="'long-'+index">{{ rec }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const analysisType = ref('competitive_analysis');
const params = ref({
  company: '',
  industry: '',
  timeframe: ''
});
const results = ref(null);
const loading = ref(false);
const error = ref('');

const analyze = async () => {
  try {
    loading.value = true;
    error.value = '';
    
    const response = await axios.post('http://localhost:5000/analyze', {
      type: analysisType.value,
      params: params.value
    });

    if (response.data.error) {
      throw new Error(response.data.error);
    }

    results.value = response.data.data;
  } catch (err) {
    error.value = err.response?.data?.error || err.message;
    results.value = null;
  } finally {
    loading.value = false;
  }
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.query-section {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
}

.btn-primary {
  background: #007bff;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.results-section {
  margin-top: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.competitor-card {
  margin: 1rem 0;
  padding: 1rem;
  border-left: 4px solid #007bff;
  background: #f8f9fa;
}

.error-message {
  color: #dc3545;
  padding: 1rem;
  margin: 1rem 0;
  border: 1px solid #dc3545;
  border-radius: 4px;
}

.loading {
  padding: 1rem;
  text-align: center;
  color: #6c757d;
}

.recommendation-type {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

ul {
  list-style-type: disc;
  padding-left: 2rem;
}
</style>