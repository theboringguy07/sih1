from rapidfuzz import fuzz
import re

class RecommendationEngine:
    def __init__(self):
        self.education_weights = {
            'btech': ['engineering', 'technology', 'software', 'it'],
            'bsc': ['science', 'research', 'lab', 'analysis'],
            'bcom': ['finance', 'banking', 'accounting', 'business'],
            'ba': ['content', 'writing', 'communication', 'media'],
            'mba': ['management', 'business', 'strategy', 'operations'],
            'diploma': ['technical', 'skill-based', 'vocational'],
            '12th': ['entry-level', 'training', 'basic']
        }
        
        self.location_preference_weight = 0.3
        self.skills_match_weight = 0.3
        self.education_match_weight = 0.2
        self.interests_match_weight = 0.2

    def get_recommendations(self, user_data, internships):
        """
        Get top 3-5 internship recommendations based on user profile
        """
        scores = []
        
        for internship in internships:
            score = self._calculate_match_score(user_data, internship)
            scores.append({
                'internship': internship,
                'score': score
            })
        
        # Sort by score (descending) and return top 5
        scores.sort(key=lambda x: x['score'], reverse=True)
        recommendations = []
        
        for item in scores[:5]:
            recommendation = item['internship'].copy()
            recommendation['match_score'] = round(item['score'], 2)
            recommendation['match_reasons'] = self._get_match_reasons(user_data, item['internship'])
            recommendations.append(recommendation)
        
        return recommendations

    def _calculate_match_score(self, user_data, internship):
        """
        Calculate match score between user and internship
        """
        total_score = 0
        
        # Education match
        education_score = self._calculate_education_match(
            user_data.get('education', '').lower(),
            internship.get('requirements', {}).get('education', '').lower(),
            internship.get('sector', '').lower()
        )
        total_score += education_score * self.education_match_weight
        
        # Skills match
        skills_score = self._calculate_skills_match(
            user_data.get('skills', []),
            internship.get('requirements', {}).get('skills', [])
        )
        total_score += skills_score * self.skills_match_weight
        
        # Location preference
        location_score = self._calculate_location_match(
            user_data.get('location', ''),
            internship.get('location', '')
        )
        total_score += location_score * self.location_preference_weight
        
        # Interests match
        interests_score = self._calculate_interests_match(
            user_data.get('interests', []),
            internship.get('sector', ''),
            internship.get('description', '')
        )
        total_score += interests_score * self.interests_match_weight
        
        return total_score * 100  # Convert to percentage

    def _calculate_education_match(self, user_education, required_education, sector):
        """
        Calculate education match score
        """
        if not user_education or not required_education:
            return 0.5  # Default score if missing data
        
        # Direct match
        if fuzz.partial_ratio(user_education, required_education) > 80:
            return 1.0
        
        # Check if user's education aligns with sector
        education_key = self._extract_education_level(user_education)
        if education_key in self.education_weights:
            relevant_sectors = self.education_weights[education_key]
            for relevant_sector in relevant_sectors:
                if fuzz.partial_ratio(relevant_sector, sector) > 60:
                    return 0.8
        
        return 0.3  # Low but not zero score for different education

    def _calculate_skills_match(self, user_skills, required_skills):
        """
        Calculate skills match score
        """
        if not user_skills or not required_skills:
            return 0.3
        
        matches = 0
        total_required = len(required_skills)
        
        for required_skill in required_skills:
            for user_skill in user_skills:
                if fuzz.partial_ratio(user_skill.lower(), required_skill.lower()) > 75:
                    matches += 1
                    break
        
        return matches / total_required if total_required > 0 else 0

    def _calculate_location_match(self, user_location, internship_location):
        """
        Calculate location preference match
        """
        if not user_location or not internship_location:
            return 0.5
        
        # Exact match
        if fuzz.ratio(user_location.lower(), internship_location.lower()) > 80:
            return 1.0
        
        # Same state/region
        if fuzz.partial_ratio(user_location.lower(), internship_location.lower()) > 60:
            return 0.7
        
        # Remote work preference
        if 'remote' in user_location.lower() and 'remote' in internship_location.lower():
            return 1.0
        
        return 0.2  # Different location

    def _calculate_interests_match(self, user_interests, sector, description):
        """
        Calculate interests match with internship sector and description
        """
        if not user_interests:
            return 0.5
        
        combined_text = f"{sector} {description}".lower()
        matches = 0
        
        for interest in user_interests:
            if fuzz.partial_ratio(interest.lower(), combined_text) > 50:
                matches += 1
        
        return min(matches / len(user_interests), 1.0)

    def _extract_education_level(self, education):
        """
        Extract education level from education string
        """
        education_lower = education.lower()
        
        patterns = {
            'btech': r'b\.?tech|bachelor.*technology|engineering',
            'bsc': r'b\.?sc|bachelor.*science',
            'bcom': r'b\.?com|bachelor.*commerce',
            'ba': r'\bba\b|bachelor.*arts',
            'mba': r'mba|master.*business',
            'diploma': r'diploma|polytechnic',
            '12th': r'12th|class.*12|higher.*secondary|intermediate'
        }
        
        for key, pattern in patterns.items():
            if re.search(pattern, education_lower):
                return key
        
        return 'unknown'

    def _get_match_reasons(self, user_data, internship):
        """
        Generate human-readable reasons for the match
        """
        reasons = []
        
        # Education match
        if fuzz.partial_ratio(
            user_data.get('education', '').lower(),
            internship.get('requirements', {}).get('education', '').lower()
        ) > 70:
            reasons.append("Educational background matches requirements")
        
        # Skills match
        user_skills = user_data.get('skills', [])
        required_skills = internship.get('requirements', {}).get('skills', [])
        matched_skills = []
        
        for required_skill in required_skills:
            for user_skill in user_skills:
                if fuzz.partial_ratio(user_skill.lower(), required_skill.lower()) > 75:
                    matched_skills.append(user_skill)
                    break
        
        if matched_skills:
            reasons.append(f"Skills match: {', '.join(matched_skills[:3])}")
        
        # Location match
        if fuzz.partial_ratio(
            user_data.get('location', '').lower(),
            internship.get('location', '').lower()
        ) > 60:
            reasons.append("Location preference matches")
        
        # Interests match
        user_interests = user_data.get('interests', [])
        sector = internship.get('sector', '')
        matched_interests = []
        
        for interest in user_interests:
            if fuzz.partial_ratio(interest.lower(), sector.lower()) > 50:
                matched_interests.append(interest)
        
        if matched_interests:
            reasons.append(f"Interest alignment: {', '.join(matched_interests)}")
        
        return reasons[:3]  # Return top 3 reasons
