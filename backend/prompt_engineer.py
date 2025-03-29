TEMPLATES = {
    'analysis': {
        'system_role': "act as a senior business analyst with expertise in market intelligence and company.",
        'structure': """{
            'overview': 'text',
            'competitors': [
                {
                    'name': 'string',
                    'market_share': 'percentage',
                    'strength': ['list'],
                    'weakness': ['list']
                }
            ],
            'recommendation': {
                'short_term': ['list'],
                'long_term': ['list']
            }
        }"""
    }
}

class PromptBuilder:
    @staticmethod
    def create_prompt(query_type: str, params: dict) -> str:
        template = TEMPLATES[query_type]
        return f"""
        {template['system_role']}
        
        Analyze {params.get('company')} in the {params.get('industry')} industry.
        Follow this struture EXACTLY:
        {template['structure']}
        
        key considerations:
        - include both quantitive and qualitative factors
        - compare against industry benchmarks
        - prioritize actionable recommendations
        - use professional business terminology
        """


